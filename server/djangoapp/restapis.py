import requests
import os
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

# Use correct keys from .env
backend_url = os.getenv('backend_url', default="http://localhost:3030")
sentiment_analyzer_url = os.getenv('sentiment_analyzer_url', default="http://localhost:5050/")

# -------------------------------
# GET request to backend microservice
# -------------------------------
def get_request(endpoint, **kwargs):
    params = ""
    if kwargs:
        for key, value in kwargs.items():
            params += key + "=" + value + "&"

    request_url = backend_url + endpoint + "?" + params
    print("GET from {} ".format(request_url))

    try:
        response = requests.get(request_url)
        return response.json()
    except Exception as e:
        print(f"GET request failed: {e}")
        return None

# -------------------------------
# Call sentiment analyzer microservice
# -------------------------------
def analyze_review_sentiments(text):
    request_url = sentiment_analyzer_url + "analyze/" + text
    print("Calling sentiment analyzer at:", request_url)
    try:
        response = requests.get(request_url)
        return response.json()
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        print("Network exception occurred")
        return {"label": "unknown"}

def post_review(data_dict):
    request_url = backend_url + "/insert_review"
    try:
        response = requests.post(request_url, json=data_dict)
        print(response.json())
        return response.json()
    except Exception as e:
        print(f"POST request failed: {e}")
        print("Network exception occurred")
        return {"error": "Network issue"}
