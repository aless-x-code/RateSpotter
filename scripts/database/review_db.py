import sys
from pathlib import Path
import pprint

# Add the project root to sys.path
current_file = Path(__file__).resolve()
project_root = current_file.parents[2]  # Adjust based on your directory depth
sys.path.append(str(project_root))

from scripts.reviews import get_tripadvisor_reviews_from_api
from auth import mongodb_client


customer_reviews_db = mongodb_client["customer_reviews_db"] 
tripadvisor_reviews = customer_reviews_db["tripadvisor_reviews"]


def foo():
    result = tripadvisor_reviews.insert_one({ "Rating" : "2" })
    print(result.acknowledged)

    # pprint.pp(get_tripadvisor_reviews_from_api())

if __name__ == "__main__":
    foo()


