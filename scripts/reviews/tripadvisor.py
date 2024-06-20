import requests
from pathlib import Path
from dotenv import load_dotenv
import os



def get_tripadvisor_reviews_from_api():
    load_dotenv()

    tripadv_api_k = os.environ.get("tripadv_api_k")
    url = f"https://api.content.tripadvisor.com/api/v1/location/2314754/reviews?language=en&key={tripadv_api_k}"
    headers = {"accept": "application/json"}

    response = requests.get(url, headers=headers)

    review_dict = parse_tripadvisor_reviews(response.json())

    return review_dict


def parse_tripadvisor_reviews(data):
    review_dict = {"review_1": {}, "review_2": {}, "review_3": {}}


    for i, review_key in enumerate(review_dict.keys()):
        review_dict[review_key]["link"] = data["data"][i]["url"]
        review_dict[review_key]["review_id"] = data["data"][i]["id"]
        review_dict[review_key]["rating"] = data["data"][i]["rating"]
        review_dict[review_key]["posting_date"] = data["data"][i]["published_date"]


    return review_dict


def foo():
    pass

if __name__ == "__main__":
    foo()
    