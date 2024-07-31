from pymongo import DESCENDING
import logging

from scripts.reviews import (get_and_format_tripadvisor_reviews_from_api, 
                             get_and_format_yelp_reviews_from_api, 
                             get_and_format_google_reviews_from_api)
from settings import reviews_to_store

class ReviewManager:

    def __init__(self, platform_name, review_collection):
        self.platform_name = platform_name
        self.dashboard_name = platform_name.capitalize()
        self.review_collection = review_collection
        self.review_count = self.count_reviews()
        self.api_most_recent_date = self.get_api_most_recent_date() 
        self.collection_most_recent_date = self.get_collection_most_recent_date()
        
        self.update_reviews()
        print('object created ' + platform_name)

    def get_api_reviews(self):
        try:
            if self.platform_name == 'google':
                return get_and_format_google_reviews_from_api()
            elif self.platform_name == 'tripadvisor':
                return get_and_format_tripadvisor_reviews_from_api()
            elif self.platform_name == 'yelp':
                return get_and_format_yelp_reviews_from_api()
            raise ValueError(f"Unsupported platform: {self.platform_name}")
        
        except ValueError as ve:
            logging.error(f"Unsupported platform: {self.platform_name}. Additional notes: {ve}")
            return []
        except Exception as e:
            logging.error(f"An error occurred while fetching API reviews: {e}")
            return []

    def get_collection_most_recent_date(self):
        try:
            if self.review_count == 0:
                return 0
            
            reviews = self.review_collection.find({'platform_name' : f'{self.platform_name}' }, 
                                                max_time_ms=10000, 
                                                limit=reviews_to_store, 
                                                sort=[("post_date", DESCENDING)])

            return reviews[0]['post_date']
        except IndexError:
            logging.error(f"No reviews found for platform: {self.platform_name}")
            return None
        except Exception as e:
            logging.error(f"An error occurred while fetching collection reviews: {e}")
            return None
        
    def get_api_most_recent_date(self):
        try:
            api_reviews = self.get_api_reviews()
            if api_reviews:
                return api_reviews[0]['post_date']
            return None
        except Exception as e:
            logging.error(f"An error occurred while fetching API most recent date: {e}")
            return None

    def count_reviews(self):
        try:
            return self.review_collection.count_documents({'platform_name': self.platform_name})
        except Exception as e:
            logging.error(f"An error occurred while counting reviews: {e}")
            return 0
    
    def write_api_reviews(self):
        try:
            reviews = self.get_api_reviews()

            for i in range(reviews_to_store):
                self.review_collection.insert_one(reviews[i])
            
            self.review_count = self.count_reviews()

        except Exception as e:
            logging.error(f"An error occurred while writing API reviews: {e}")


    def update_reviews(self):
        try: 
            if self.review_count == 0:
                self.write_api_reviews()
            elif self.api_most_recent_date != self.collection_most_recent_date:
                self.delete_reviews()
                self.write_api_reviews()
            
        except Exception as e:
            logging.error(f"An error occurred while updating reviews: {e}")
    
    def delete_reviews(self):
        try:
            self.review_collection.delete_many({'platform_name' : f'{self.platform_name}' }, comment="Deleting reviews")
            self.review_count = self.count_reviews()

        except Exception as e:
            logging.error(f"An error occurred while deleting reviews: {e}")

    def update_and_get_reviews(self):
        try:
            self.update_reviews()

            reviews = self.review_collection.find({'platform_name' : f'{self.platform_name}' }, 
                                                  max_time_ms=10000, 
                                                  limit=reviews_to_store, 
                                                  sort=[("post_date", DESCENDING)])

            return reviews
        
        except Exception as e:
            logging.error(f"An error occurred while updating and retrieving reviews: {e}")
            return []


