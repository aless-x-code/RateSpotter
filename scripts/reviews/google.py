import serpapi 
from dotenv import load_dotenv
import os
import uuid
import logging

from auth import users_credentials
from flask_login import current_user
from settings import reviews_to_store


load_dotenv()
SERP_API_KEY = os.environ.get("serp_api_k")

def get_google_id(restaurant_name, restaurant_address):
    if not SERP_API_KEY:
        logging.error("SerpApi key is not set.")
        return None

    try: 
        client = serpapi.Client(api_key=SERP_API_KEY)
        results = client.search(params = {
            "engine": "google_maps",
            "type": "search",
            "google_domain": "google.com",
            "q": f"{restaurant_name} + {restaurant_address}",
            "hl": "en",
            "gl": "us"
        })

        unique_match_place_id = results.get('place_results', {}).get('place_id')
        if unique_match_place_id:
            return unique_match_place_id

        best_match_place_id = results.get('local_results', [{}])[0].get('place_id')
        if best_match_place_id:
            return best_match_place_id
    
    except KeyError as e:
        logging.error(f"KeyError occurred while fetching Google ID: {e}")
    except IndexError as e:
        logging.error(f"IndexError occurred while fetching Google ID: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred while fetching Google ID: {e}")

    return None

def get_and_format_google_reviews_from_api():
    if not SERP_API_KEY:
        logging.error("SerpApi key is not set.")
        return []
    
    try:
        user = users_credentials.find_one({'username': current_user.username})
        if not user:
            logging.error(f"User not found: {current_user.username}")
            return []
        
        google_id = user.get('google_id')
        if not google_id:
            logging.error(f"Yelp ID not found for user: {current_user.username}")
            return []

        client = serpapi.Client(api_key=SERP_API_KEY)
        reviews = client.search({
            "engine": "google_maps_reviews",
            "hl": "en",
            "place_id": f"{google_id}",
            "sort_by": "newestFirst"
        })
        reviews = format_google(reviews)
    
        return reviews
    
    except Exception as e:
        logging.error(f"An unexpected error occurred while getting and formatting Google reviews from API: {e}")
        return []

def format_google(api_reviews):
    reviews = []

    try:
        for i in range(reviews_to_store):
            review = api_reviews["reviews"][i]
            user = review.get('user', {})

            reviews.append({
                'platform_name': 'google',
                "review_id": str(uuid.uuid4()),
                "post_date": review.get('iso_date_of_last_edit', 'None'),
                "user": user.get('name', 'N/A'),
                "avatar": user.get('thumbnail', ''),
                "rating": review.get('rating', 0),
                "title": "N/A",
                "text": review.get('snippet', '')
            })
        return reviews
    
    except IndexError:
        logging.error(f"Not enough reviews in the Google API response. Requested: {reviews_to_store}, Available: {len(api_reviews['reviews'])}")
        return reviews 
    except Exception as e:
        logging.error(f"An unexpected error occurred while formatting Google API reviews: {e}")
        return []

