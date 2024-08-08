import serpapi 
from dotenv import load_dotenv
import os
import uuid
import logging

from settings import reviews_to_store
from auth import users_credentials
from flask_login import current_user


load_dotenv()
SERP_API_KEY = os.environ.get("serp_api_k")

def get_yelp_id(restaurant_name, restaurant_address):
    if not SERP_API_KEY:
        logging.error("SerpApi key is not set.")
        return None

    try: 
        client = serpapi.Client(api_key=SERP_API_KEY)
        results = client.search({
            "engine": "yelp",
            "find_loc": f"{restaurant_address}",
            "find_desc": f"{restaurant_name}",
            "yelp_domain": "www.yelp.com",
            "sortby": "recommended"
        })

        FIRST_RESULT = 0
        YELP_ID_INDEX = 0

        if 'organic_results' not in results or not results['organic_results']:
            logging.error(f"No Yelp API results found for {restaurant_name} at {restaurant_address}")
            return None
        
        yelp_id = results['organic_results'][FIRST_RESULT].get('place_ids', [None])[YELP_ID_INDEX]

        if not yelp_id:
            logging.error(f"Yelp ID not found for {restaurant_name} at {restaurant_address}")
            return None

        return yelp_id

    except IndexError as e:
        logging.error(f"Index error occurred while fetching Yelp ID: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred while getting Yelp ID: {e}")
    
    return None

def get_and_format_yelp_reviews_from_api():
    if not SERP_API_KEY:
        logging.error("SerpApi key is not set.")
        return []
    
    try: 
        user = users_credentials.find_one({'username': current_user.username})
        if not user:
            logging.error(f"User not found: {current_user.username}")
            return []
        
        yelp_id = user.get('yelp_id')
        if not yelp_id:
            logging.error(f"Yelp ID not found for user: {current_user.username}")
            return []

        client = serpapi.Client(api_key=SERP_API_KEY)
        reviews = client.search({
            'engine': 'yelp_reviews',
            "place_id": yelp_id,
            "yelp_domain": "www.yelp.com",
            "hl": "en",
            "sortby": "date_desc"
        })
        reviews = format_yelp(reviews)

        return reviews
    
    except Exception as e:
        logging.error(f"An unexpected error occurred while getting and formatting Yelp reviews from API: {e}")
        return []



def format_yelp(api_reviews):
    reviews = []

    try:
        for i in range(reviews_to_store):
            review = api_reviews["reviews"][i]
            user = review.get('user', {})
            comment = review.get('comment', {})

            reviews.append({
                'platform_name': 'yelp',
                "review_id": str(uuid.uuid4()),
                "post_date": review.get('date', 0),
                "user": user.get('name', 'None'),
                "avatar": user.get('thumbnail', ''),
                "rating": review.get('rating', 0),
                "title": "N/A",
                "text": comment.get('text', 'None')
            })
        return reviews
    
    except IndexError:
        logging.error(f"Not enough reviews in the Yelp API response. Requested: {reviews_to_store}, Available: {len(api_reviews['reviews'])}")
        return reviews 
    except Exception as e:
        logging.error(f"An unexpected error occurred while formatting Yelp API reviews: {e}")
        return []


