import requests
from dotenv import load_dotenv
import os
import pprint


def get_tripadvisor_reviews_from_api(restaurant_id):
    load_dotenv()

    key = os.environ.get("tripadv_api_k")
    url = f"https://api.content.tripadvisor.com/api/v1/location/{restaurant_id}/reviews?language=en&limit=3&key={key}"
    headers = {"accept": "application/json"}

    response = requests.get(url, headers=headers)
    
    reviews = format_tripadvisor(response.json())
    
    return reviews


def format_tripadvisor(data):
    reviews = {"review_1": {}, "review_2": {}, "review_3": {}}

    for i, review_key in enumerate(reviews.keys()):
        reviews[review_key]["review_id"] = data["data"][i]["id"]
        reviews[review_key]["post_date"] = data["data"][i]["published_date"]
        reviews[review_key]["link"] = data["data"][i]["url"]
        reviews[review_key]["language"] = data["data"][i]["lang"]
        reviews[review_key]["user"] = data["data"][i]["user"]["username"]
        reviews[review_key]["avatar_small"] = data["data"][i]["user"]["avatar"]["small"]
        reviews[review_key]["rating"] = data["data"][i]["rating"]
        reviews[review_key]["title"] = data["data"][i]["title"]
        reviews[review_key]["text"] = data["data"][i]["text"]
        
    return reviews

# if __name__ == "__main__":
#     pprint.pp(get_tripadvisor_reviews_from_api())