import json
import string
import secrets
import time
import io
import boto3
import yaml
from meesho.link_scrapper import product_url_scrapper
from meesho.details_scrapper import details_scrapper
from meesho.review_scrapper_product import review_scrapper_product
from models.fake_detection_model.xgBoost.fake_comment_detection import predict
from meesho.review_scrapper_seller import review_scrapper_seller
from src.fake_score import fake_score_seller,fake_score_product, merge
from scoring.meesho_scoring import scoring_meesho
from src.score_plot import result_plot

def load_aws_credentials(file_path):
    try:
        with open(file_path, 'r') as file:
            credentials = yaml.safe_load(file)
            return credentials['aws']['access_key'], credentials['aws']['secret_key']
    except yaml.YAMLError as e:
        print(f"Error loading YAML file: {e}")
        raise
    except KeyError as e:
        print(f"Missing key in the YAML file: {e}")
        raise

def generate_uids(count, length=15):
    # Precompute the character pool
    characters = string.ascii_letters + string.digits

    # Generate unique UIDs
    uids = set()
    while len(uids) < count:
        uid = ''.join(secrets.choice(characters) for _ in range(length))
        uids.add(uid)
    return list(uids)

aws_access_key, aws_secret_key = load_aws_credentials('keys.yaml')
timestamp = time.strftime("%Y%m%d")
search_string = "laptop stand"
# search_string = input('Enter the Product name: ')
bucket_name = 'marketplace-scanner'
folder_name = f"Meesho/Meesho_{search_string}_{timestamp}"

product_links = product_url_scrapper(meesho_url="https://www.meesho.com/", search_string=search_string, country_code="IN")
uids = generate_uids(count=len(product_links), length=15)

s3_client = boto3.client('s3', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key,
                         region_name='ap-south-1')

data_dict = {}

for uid, links in zip(uids, product_links):
    data_dict[f"{uid}"] = {}
    data_dict[f"{uid}"]["Product_url"] = f"{links}"


# Iterate through keys and values in the JSON data
for key, value in data_dict.items():
    print(f"Key: {key},")
    print(value.get("Product_url"))
    name, rating_value, price_discounted, price_actual, seller_name, list_service, seller_rating, image_url, product_description_text, discount_text = details_scrapper(url=value.get("Product_url"))
    details = {
        "name": name,
        "rating_value": rating_value,
        "price_discounted": price_discounted,
        "price_actual": price_actual,
        "discount": discount_text,
        "seller_name": seller_name,
        "seller_rating" : seller_rating,
        # "seller_links": seller_links,
        "list_service": list_service,
        "image_url": image_url,
        "product_description" : product_description_text

    }
    value["details"] = details

updated_json_string = json.dumps(data_dict, indent=4)

s3_client.upload_fileobj(io.BytesIO(updated_json_string.encode('utf-8')), bucket_name,
                         f"{folder_name}/{search_string}_details.json")

reviews_product_data = review_scrapper_product(data_dict)
reviews_json_buffer_prod = io.BytesIO()
json_string_product = json.dumps(reviews_product_data, indent=4)
reviews_json_buffer_prod.write(json_string_product.encode('utf-8'))
reviews_json_buffer_prod.seek(0)
s3_client.upload_fileobj(reviews_json_buffer_prod, bucket_name,
                         f"{folder_name}/{search_string}_product_comments.json")

reviews_seller_data = review_scrapper_seller(data_dict)
reviews_json_buffer_seller = io.BytesIO()
json_string_seller = json.dumps(reviews_seller_data, indent=4)
reviews_json_buffer_seller.write(json_string_seller.encode('utf-8'))
reviews_json_buffer_seller.seek(0)
s3_client.upload_fileobj(reviews_json_buffer_seller, bucket_name,
                         f"{folder_name}/{search_string}_seller_comments.json")

predictions_prod = predict(reviews_product_data)
predictions_json_buffer = io.BytesIO()
json_string_pred_prod = json.dumps(predictions_prod, indent=4)
predictions_json_buffer.write(json_string_pred_prod.encode('utf-8'))
predictions_json_buffer.seek(0)
s3_client.upload_fileobj(predictions_json_buffer, bucket_name,
                         f"{folder_name}/{search_string}_product_review_prediction.json")

predictions_seller = predict(reviews_seller_data)
predictions_json_buffer1 = io.BytesIO()
json_string_pred_seller = json.dumps(predictions_seller, indent=4)
predictions_json_buffer1.write(json_string_pred_seller.encode('utf-8'))
predictions_json_buffer1.seek(0)
s3_client.upload_fileobj(predictions_json_buffer1, bucket_name,
                         f"{folder_name}/{search_string}_seller_review_prediction.json")

# Generate fake score based on product details and review predictions
fake_score_results = fake_score_product(
    details=updated_json_string,
    product_review=json_string_product,
    product_review_prediction=json_string_pred_prod
)

result_data = json.loads(json.dumps(fake_score_results))

# Generate and merge seller fake score
data = fake_score_seller(seller_review=json_string_seller, seller_review_prediction=json_string_pred_seller)
result_data_seller = json.loads(json.dumps(data))

if isinstance(fake_score_results, str):
    result_data = json.loads(fake_score_results)

# Merge seller data and update main result_data
for key, value in result_data.items():
    seller_name = value.get("seller_name")
    if seller_name is not None:
        Comment_Count_Seller, Fake_Comment_Count_Seller = merge(data=result_data_seller,
                                                                seller_name_input=seller_name)
        value["Comment_Count_Seller"] = Comment_Count_Seller
        value["Fake_Comment_Count_Seller"] = Fake_Comment_Count_Seller

updated_json_string = json.dumps(result_data, indent=4)

scoring_results = scoring_meesho(updated_json_string)

scoring_results_buffer = io.BytesIO()
json_scoring_result = json.dumps(scoring_results, indent=4)
scoring_results_buffer.write(json_scoring_result.encode('utf-8'))
scoring_results_buffer.seek(0)
s3_client.upload_fileobj(scoring_results_buffer, bucket_name, f"{folder_name}/{search_string}_results.json")

parsed_scoring_result_json = json.dumps(scoring_results)
plot_buffer = result_plot(input_json=parsed_scoring_result_json)
s3_client.upload_fileobj(plot_buffer, bucket_name, f"{folder_name}/{search_string}_acviss_score_plot.png")