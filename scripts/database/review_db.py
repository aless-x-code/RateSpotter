import sys
from pathlib import Path
import pprint
from typing import Dict, Any, List
from pymongo import DESCENDING
from flask_login import current_user

from scripts.reviews import get_tripadvisor_reviews_from_api
from auth import client



def write_reviews(collection, reviews):
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


    collection.insert_one(review_1)
    collection.insert_one(review_2)
    collection.insert_one(review_3)


def get_tripadvisor_collection(restaurant_id):

    if current_user.is_authenticated:
        customer_database = client["customers"] 
        tripadvisor_collection = customer_database[f"{current_user.username}_tripadvisor_collection"]

        if tripadvisor_collection.count_documents({}) != 0:
            api_reviews = get_tripadvisor_reviews_from_api(restaurant_id)
            api_most_recent = api_reviews["review_1"]["post_date"]

            
            collection_most_recent = tripadvisor_collection.find_one({}, sort=[("post_date", DESCENDING)])["post_date"]

            if api_most_recent != collection_most_recent:
                write_reviews(tripadvisor_collection, api_reviews)
        elif tripadvisor_collection.count_documents({}) == 0:
            api_reviews = get_tripadvisor_reviews_from_api(restaurant_id)
            write_reviews(tripadvisor_collection, api_reviews)
        
        all_reviews = tripadvisor_collection.find({}, max_time_ms=10000, limit=3)

        return all_reviews
    

    return None
    


# if __name__ == "__main__":
#     get_tripadvisor_collection()


