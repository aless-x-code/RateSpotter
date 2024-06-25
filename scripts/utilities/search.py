import requests
from dotenv import load_dotenv
import os
import pprint

def search_restaurants(restaurant_name, restaurant_zip_code):
    load_dotenv()
    key = os.environ.get("tripadv_api_k")
    url = f"https://api.content.tripadvisor.com/api/v1/location/search?key={key}&searchQuery={restaurant_name}&address={restaurant_zip_code}&language=en"
    # url = f"https://api.content.tripadvisor.com/api/v1/location/search?key={key}&searchQuery={restaurant_name}&address={restaurant_zip_code}&phone={phone_number}&language=en"
    headers = {"accept": "application/json"}

    api_results = requests.get(url, headers=headers).json()

    matching_restaurants = []

    for i, entry in enumerate(api_results['data']):
        formatted_entry = {
            'location_id': entry["location_id"],  # id as a string, starting from '1'
            'name': entry['name'],  # name of the location
            'address': entry['address_obj']['address_string']  # zip code from address_obj
        }
        matching_restaurants.append(formatted_entry)

    return matching_restaurants


def get_restaurant_by_id(location_id):

    load_dotenv()
    key = os.environ.get("tripadv_api_k")
    url = f"https://api.content.tripadvisor.com/api/v1/location/{location_id}/details?key={key}&language=en&currency=USD"
    headers = {"accept": "application/json"}

    api_results = requests.get(url, headers=headers).json()

    restaurant = {}
    restaurant["location_id"] = api_results["location_id"]
    restaurant["name"] = api_results["name"]
    restaurant["address"] = api_results['address_obj']['address_string']

    return restaurant

# if __name__ == "__main__":
#     pprint.pprint(get_restaurant_by_id(13504265))
