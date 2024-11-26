import json
from src.sentence_score import sentence_score
import os
from langchain_groq import ChatGroq
def fake_score_product(details, product_review, product_review_prediction):
    details_data = json.loads(details)
    product_review_data = json.loads(product_review)
    product_review_prediction_data = json.loads(product_review_prediction)

    result = {}
    os.environ["GROQ_API_KEY"] = "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"
    model = ChatGroq(model="Gemma2-9b-it")
    for key, value in details_data.items():
        result[f"{key}"] = {}
        Product_url = value.get("Product_url")
        product_rating = value.get("details").get("rating_value")
        seller_name = value.get("details").get("seller_name")
        seller_rating = value.get("details").get("seller_rating")
        product_description = value.get("details").get("product_description")
        discount = value.get("details").get("discount")
        list_service = value.get("details").get("list_service")

        try:
            if "7-day Returns" in list_service:
                return_policy = True
            else:
                return_policy = False
        except:
            return_policy = False

        if product_description is not None:
            Sentence_score = sentence_score(text=product_description, model=model)
        else:
            Sentence_score = None
        result[f"{key}"]["Product_url"] = Product_url
        result[f"{key}"]["product_rating"] = product_rating
        result[f"{key}"]["discount"] = discount
        result[f"{key}"]["seller_name"] = seller_name
        result[f"{key}"]["seller_rating"]= seller_rating
        result[f"{key}"]["return_policy"] = return_policy
        result[f"{key}"]["Sentence_score"] = Sentence_score

    for key, value in product_review_data.items():


        reviews = value.get("reviews")

        review_list = []
        try:
            for review in reviews:
                review_list.append(review)
        except:
            pass

        result[f"{key}"]["Comment Count Product"] = len(review_list)

    for key, values in product_review_prediction_data.items():
        fake_comment = []
        for value in values:
            fake_comment.append(value.get("comment"))

        result[f"{key}"]["Fake Comment Count Product"] = len(fake_comment)
    updated_json_string = json.dumps(result, indent=4)

    return updated_json_string


def merge(data, seller_name_input):
    for key, value in data.items():
        seller_name = value.get("seller_name")
        Comment_Count_Seller = value.get("Comment Count Seller")
        Fake_Comment_Count_Seller = value.get("Fake Comment Count Seller")
        if seller_name_input==seller_name:
            return Comment_Count_Seller, Fake_Comment_Count_Seller


def fake_score_seller(seller_review, seller_review_prediction):

    seller_review = json.loads(seller_review)
    seller_review_prediction = json.loads(seller_review_prediction)

    result = {}

    for key, value in seller_review.items():

        review_list = []
        reviews = value.get("reviews")
        seller_name = value.get("seller_name")
        result[f"{key}"] = {}
        for review in reviews:
            review_list.append(review)


        result[f"{key}"]["seller_name"] = seller_name
        result[f"{key}"]["Comment Count Seller"] = len(review_list)


    for key, values in seller_review_prediction.items():
        fake_comment = []
        for value in values:
            fake_comment.append(value.get("comment"))

        result[f"{key}"]["Fake Comment Count Seller"] = len(fake_comment)

    return result
