# Uncomment the imports below before you add the function code
import requests
import os
from dotenv import load_dotenv

load_dotenv()

backend_url = os.getenv(
    'backend_url', default="http://localhost:3030")
sentiment_analyzer_url = os.getenv(
    'sentiment_analyzer_url',
    default="http://localhost:5050/")


def get_request(endpoint, **kwargs):
    params = ""
    if kwargs:
        for key, value in kwargs.items():
            params = params + key + "=" + str(value) + "&"

    request_url = backend_url + endpoint + "?" + params

    print(f"GET from {request_url}")
    try:
        response = requests.get(request_url)
        return response.json()
    except Exception:
        print("Network exception occurred")
        return None


def analyze_review_sentiments(text):
    request_url = sentiment_analyzer_url + "analyze/" + text
    try:
        response = requests.get(request_url)
        return response.json()
    except Exception:
        print("Network exception occurred when analyzing sentiment")
        return None


def post_review(data_dict):
    request_url = backend_url + "/insert_review"
    try:
        response = requests.post(request_url, json=data_dict)
        return response.json()
    except Exception:
        print("Network exception occurred when posting review")
        return None


def get_dealers_from_cf(endpoint):
    results = []
    json_result = get_request(endpoint)
    if json_result:
        dealers = json_result if isinstance(json_result, list) else json_result.get("data", [])
        for dealer in dealers:
            results.append(dealer)
    return results


def get_dealer_by_id_from_cf(endpoint, dealer_id):
    json_result = get_request(endpoint)
    if json_result and len(json_result) > 0:
        return json_result[0]
    return {}


def get_dealer_reviews_from_cf(endpoint):
    results = []
    json_result = get_request(endpoint)
    if json_result:
        reviews = json_result if isinstance(json_result, list) else json_result.get("data", [])
        for review in reviews:
            results.append(review)
    return results