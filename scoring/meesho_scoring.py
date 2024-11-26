import json
from logger.logs import logger_info, logger_error
import re


def extract_numbers(input_string):
    # Find all numbers (both integers and floats)
    numbers = re.findall(r"\d*\.\d+|\d+", input_string)
    # Convert extracted strings to float or int
    converted_numbers = [float(num) if '.' in num else int(num) for num in numbers]

    return converted_numbers[0]


def fake_comment_calculation(total_comments, fake_comments):
    if fake_comments == 0 or fake_comments == None:
        contribution_score = 15

    elif total_comments == 0 or total_comments == None:
        contribution_score = 7.5
    else:
        ratio = fake_comments / total_comments
        score = (1 - ratio) * 5
        contribution_score = (score / 5) * 15

    return contribution_score


"""
Product Rating: 20%
Seller Rating: 20%
Return Policy: 10%
Sentence Score: 10%
Fake Comment Ratio for Product: 15%
Fake Comment Ratio for Seller: 15%
Discount: 10%
"""

def scoring_meesho(result_data):

    if isinstance(result_data, str):
        result_data = json.loads(result_data)

    results = {}
    for key, value in result_data.items():
        Default_product_rating = 3
        Default_seller_rating = 3
        Default_return_policy = False
        Default_Sentence_score = 2  # here we consider good product supposed to have good description
        ##### product rating calculation

        product_rating = value["product_rating"]
        try:
            product_rating = product_rating.strip()
        except:
            pass
        # Check if the string is empty, and if so, set a default value of 3
        if not product_rating:

            product_rating = Default_product_rating  # Default value for empty input
            logger_info(f"Product rating default value Due to null for key {key}, {result_data}")

        else:
            try:
                # Try to convert to an integer
                product_rating = int(product_rating)
            except ValueError:
                try:
                    product_rating = float(product_rating)
                except ValueError:
                    product_rating = Default_product_rating  # Default value if invalid input
                    logger_info(f"product rating default invalid value key {key}, {result_data}")

            # Check if product rating is greater than 5, and if so, set it to 3
            if product_rating > 5:
                logger_info(f"Product rating default value value greater than 5 key {key}, {result_data}")

                product_rating = Default_product_rating

        acviss_score_product_rating = (product_rating / 5) * 20

        ##### seller rating calculation

        seller_rating = value["seller_rating"]
        if not seller_rating:
            seller_rating = Default_seller_rating

            logger_info(f"seller rating default value Due to null for key {key}, {result_data}")
        else:
            try:
                # Try to convert to an integer
                seller_rating = int(seller_rating)
            except ValueError:
                try:
                    seller_rating = float(seller_rating)
                except ValueError:
                    seller_rating = Default_seller_rating  # Default value if invalid input
                    logger_info(f"seller rating default invalid value key {key}, {result_data}")

            # Check if product rating is greater than 5, and if so, set it to 3
            if seller_rating > 5:
                logger_info(f"seller rating default  value greater than 5 key {key}, {result_data}")
                seller_rating = Default_seller_rating

        acviss_score_seller_rating = (seller_rating / 5) * 20

        ### return_policy calculation
        return_policy = value["return_policy"]

        if not return_policy:
            return_policy = Default_return_policy
            acviss_score_return_policy = 0
            logger_info(f"return_policy default value Due to null for key {key}, {result_data}")
        else:
            if return_policy:
                acviss_score_return_policy = 1 * 10  # Full contribution if True
            else:
                acviss_score_return_policy = 0

        ### Sentence_score calculation
        Sentence_score = value["Sentence_score"]
        if not Sentence_score:
            Sentence_score = Default_Sentence_score
            acviss_score_Sentence_score = (Sentence_score / 5) * 10
            logger_info(f"Sentence_score default value Due to null for key {key}, {result_data}")
        else:
            acviss_score_Sentence_score = (Sentence_score / 5) * 10

        ### discount calculation

        if not value["discount"]:

            acviss_score_discount = 10
        else:
            discount_percentage = extract_numbers(value["discount"])
            discount_score = 1 - (discount_percentage / 100)

            # Calculate the contribution to the final score
            acviss_score_discount = discount_score * 10

        ### "Fake Comment Count Product"
        try:
            product_comment = value["Comment Count Product"]
        except:
            product_comment = 0
        try:
            product_fake_comment_Count = value["Fake Comment Count Product"]

        except:
            product_fake_comment_Count = 0
        try:
            seller_comment = value["Comment_Count_Seller"]
        except:
            seller_comment = 0
        try:
            seller_fake_comment_Count = value["Fake_Comment_Count_Seller"]
        except:
            seller_fake_comment_Count = 0

        product_comment_score = fake_comment_calculation(total_comments=product_comment,
                                                         fake_comments=product_fake_comment_Count)
        seller_comment_score = fake_comment_calculation(total_comments=seller_comment,
                                                        fake_comments=seller_fake_comment_Count)

        acviss_Score = acviss_score_product_rating + acviss_score_seller_rating + acviss_score_return_policy + acviss_score_Sentence_score + acviss_score_discount + product_comment_score + seller_comment_score
        result_data[f"{key}"]["Acviss_Score"] = round(acviss_Score)

    updated_json_string = json.dumps(result_data)

    return result_data
