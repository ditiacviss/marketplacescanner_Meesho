import json
import joblib
from deep_translator import GoogleTranslator
import langdetect

def predict(data):

    loaded_model = joblib.load('models/fake_detection_model/xgBoost/model/xgboost_model.pkl')
    loaded_vectorizer = joblib.load('models/fake_detection_model/xgBoost/tokenizer/tfidf_vectorizer.pkl')

    translator = GoogleTranslator(source='auto', target='en')
    predict = {}

    # Process each uid and its comments
    for key, value in data.items():
        user_comments = []
        results = []

        # Check if "reviews" key is present
        if "reviews" in value:
            for review in value["reviews"]:
                # Check if the review is already in English
                try:
                    detected_language = langdetect.detect(review)
                except:
                    detected_language = 'unknown'

                # If the review is not in English, translate it
                if detected_language != 'en':
                    try:
                        translated_review = translator.translate(review)
                        print("----------------")
                        print(f"Key: {key}")
                        print(f"Original Review: {review}")
                        print(f"Translated Review: {translated_review}")
                        print("----------------")
                        user_comments.append(translated_review)
                    except:
                        print("Translation error occurred")
                        pass
                else:
                    # If the review is already in English, append as is
                    user_comments.append(review)

            # Filter out any None or empty string values from user_comments
            user_comments = [comment for comment in user_comments if comment and isinstance(comment, str)]

            if user_comments:
                new_data_tfidf = loaded_vectorizer.transform(user_comments)
                predictions = loaded_model.predict(new_data_tfidf).tolist()
                prediction_probs = loaded_model.predict_proba(new_data_tfidf).tolist()

                for review, prediction, prob in zip(user_comments, predictions, prediction_probs):
                    if prediction == 0:
                        # Probability of class 0
                        confidence = prob[0]
                        if confidence > 0.90:
                            results.append({
                                'comment': review,
                                'confidence': round(confidence, 4)
                            })

            if results:
                predict[key] = results

    # Save the results to a JSON file
    return predict
    print("Results have been saved to output_predictions.json")

