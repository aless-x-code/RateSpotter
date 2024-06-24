import sys
from pathlib import Path
import pprint
from typing import Dict, Any, List
from pymongo import DESCENDING

from scripts.reviews import get_tripadvisor_reviews_from_api
from auth import mongodb_client

customer_database = mongodb_client["customers"] 
tripadvisor_collection = customer_database["tripadvisor_reviews"]

class Review:
    def __init__(self, attributes: List[Dict[str, Any]]):
        self.attributes = attributes

def write_reviews(reviews):
    review_1 = {
        "review_id": reviews["review_1"]["review_id"],
        "post_date": reviews["review_1"]["post_date"],
        "link": reviews["review_1"]["link"],
        "language": reviews["review_1"]["language"],
        "user": reviews["review_1"]["user"],
        "avatar_small": reviews["review_1"]["avatar_small"],
        "rating": reviews["review_1"]["rating"],
        "title": reviews["review_1"]["title"],
        "text": reviews["review_1"]["text"]
        }
    review_2 = {
    "review_id": reviews["review_1"]["review_id"],
    "post_date": reviews["review_2"]["post_date"],
    "link": reviews["review_2"]["link"],
    "language": reviews["review_2"]["language"],
    "user": reviews["review_2"]["user"],
    "avatar_small": reviews["review_2"]["avatar_small"],
    "rating": reviews["review_2"]["rating"],
    "title": reviews["review_2"]["title"],
    "text": reviews["review_2"]["text"]
    }
    review_3 = {
    "review_id": reviews["review_1"]["review_id"],
    "post_date": reviews["review_3"]["post_date"],
    "link": reviews["review_3"]["link"],
    "language": reviews["review_3"]["language"],
    "user": reviews["review_3"]["user"],
    "avatar_small": reviews["review_3"]["avatar_small"],
    "rating": reviews[f"review_3"]["rating"],
    "title": reviews["review_3"]["title"],
    "text": reviews["review_3"]["text"]
    }


    tripadvisor_collection.insert_one(review_1)
    tripadvisor_collection.insert_one(review_2)
    tripadvisor_collection.insert_one(review_3)


def get_tripadvisor_collection():

    if tripadvisor_collection.count_documents({}) != 0:
        api_reviews = get_tripadvisor_reviews_from_api()
        api_most_recent = api_reviews["review_1"]["post_date"]
        collection_most_recent = tripadvisor_collection.find_one({}, sort=[("post_date", DESCENDING)])["post_date"]

        if api_most_recent != collection_most_recent:
            write_reviews(api_reviews)
    elif tripadvisor_collection.count_documents({}) == 0:
        api_reviews = get_tripadvisor_reviews_from_api()
        write_reviews(api_reviews)
    
    all_reviews = tripadvisor_collection.find({}, max_time_ms=10000, limit=3)

    return all_reviews
    


# if __name__ == "__main__":
#     get_tripadvisor_collection()


