import requests
from dotenv import load_dotenv
import os
import uuid
import logging


load_dotenv()
TRIPADVISOR_API_KEY = os.environ.get("tripadv_api_k")

def search_restaurants(restaurant_name, restaurant_zip):
    if not TRIPADVISOR_API_KEY:
        logging.error("Tripadvisor API key is not set.")
        return []
    
    try:
        url = f"https://api.content.tripadvisor.com/api/v1/location/search?key={TRIPADVISOR_API_KEY}&searchQuery={restaurant_name}&address={restaurant_zip}&language=en"
        headers = {"accept": "application/json"}

        response = requests.get(url, headers=headers)
        response.raise_for_status()  

        api_results = response.json()
        matching_restaurants = []

        for entry in api_results.get('data', []):
            formatted_entry = {
                'id': str(uuid.uuid4()),
                'name': entry.get('name', 'Unknown'),
                'address': entry.get('address_obj', {}).get('address_string', 'Unknown')
            }
            matching_restaurants.append(formatted_entry)

        return matching_restaurants
    
    except requests.exceptions.RequestException as req_err:
        logging.error(f"Request error while searching for restaurants: {req_err}")
    except Exception as e:
        logging.error(f"An unexpected error occurred while searching for restaurants: {e}")

    return []


