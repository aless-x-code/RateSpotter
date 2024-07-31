import requests
from dotenv import load_dotenv
import os
import uuid
from flask_login import current_user
import logging

from auth import users_credentials
from settings import reviews_to_store


load_dotenv()
TRIPADVISOR_API_KEY = os.environ.get("tripadv_api_k")

def get_tripadvisor_id(restaurant_name, restaurant_address):
    if not TRIPADVISOR_API_KEY:
        logging.error("Tripadvisor key is not set.")
        return None
    
    try:
        format_name = restaurant_name.lower().replace(' ', '%20')
        format_address = restaurant_address.lower().replace(' ', '%20')

        url = f"https://api.content.tripadvisor.com/api/v1/location/search?searchQuery={format_name}&address={format_address}&language=en&key={TRIPADVISOR_API_KEY}"
        headers = {"accept": "application/json"}
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            logging.error(f"Tripadvisor API request failed with status code: {response.status_code}")
            return None

        results = response.json()

        if 'data' not in results or not results['data']:
            logging.error(f"No Tripadvisor API results found for {restaurant_name} at {restaurant_address}")
            return None

        tripadvisor_id = results['data'][0].get('location_id', [None])
        if not tripadvisor_id:
            logging.error(f"Tripadvisor ID not found in API response for {restaurant_name} at {restaurant_address}")
            return None

        return tripadvisor_id
    
    except IndexError as e:
        logging.error(f"Index error occurred while fetching Tripadvisor ID: {e}")
    except Exception as e:
        logging.error(f"An unexpected error occurred while getting Tripadvisor ID: {e}")
    
    return None

def get_and_format_tripadvisor_reviews_from_api():
    if not TRIPADVISOR_API_KEY:
        logging.error("Tripadvisor key is not set.")
        return None
    
    try:
        user = users_credentials.find_one({'username': current_user.username})
        if not user:
            logging.error(f"User not found: {current_user.username}")
            return []
        
        tripadvisor_id = user.get('tripadvisor_id')
        if not tripadvisor_id:
            logging.error(f"Tripadvisor ID not found for user: {current_user.username}")
            return []
        

        url = f"https://api.content.tripadvisor.com/api/v1/location/{tripadvisor_id}/reviews?language=en&limit={reviews_to_store}&key={TRIPADVISOR_API_KEY}"
        headers = {"accept": "application/json"}

        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            logging.error(f"Tripadvisor API request failed with status code: {response.status_code}")
            return None

        results = response.json()
    
        reviews = format_tripadvisor(results)
        
        return reviews
    except Exception as e:
        logging.error(f"An unexpected error occurred while getting and formatting Tripadvisor reviews from API: {e}")
        return []


def format_tripadvisor(api_reviews):
    reviews = []
    
    try:
        for i in range(reviews_to_store):
            review = api_reviews["data"][i]
            user = review.get('user', {})

            reviews.append({
                'platform_name': 'tripadvisor',
                "review_id": str(uuid.uuid4()),
                "post_date": review.get('published_date', 0),
                "user": user.get('username', 'None'),
                "avatar": user.get('avatar', {}).get('small', ''),
                "rating": review.get('rating', 0),
                "title": "N/A",
                "text": review.get('text', 'None')
            })
        return reviews
    
    except IndexError:
        logging.error(f"Not enough reviews in the Tripadvisor API response. Requested: {reviews_to_store}, Available: {len(api_reviews['reviews'])}")
        return reviews 
    except Exception as e:
        logging.error(f"An unexpected error occurred while formatting Tripadvisor API reviews: {e}")
        return []
