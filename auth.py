import os
from dotenv import load_dotenv
from flask_login import LoginManager, UserMixin
from pymongo.mongo_client import MongoClient 
from pymongo.server_api import ServerApi 
import certifi
import secrets
import logging


load_dotenv()

mongo_pw = os.environ.get("mongo_pw")
mongo_user = os.environ.get("mongo_user")

mongo_uri = f"mongodb+srv://{mongo_user}:{mongo_pw}@ratespotter-cluster.k6gug4f.mongodb.net/?retryWrites=true&w=majority&appName=ratespotter-cluster"
mongo_client = MongoClient(mongo_uri, server_api=ServerApi('1', deprecation_errors=True), tlsCAFile=certifi.where(), tls=True)


auth_db = mongo_client[os.environ.get("auth_db")] 
users_credentials = auth_db[os.environ.get("user_credentials")]

flask_secret_key = os.environ.get("FLASK_SECRET_KEY") or secrets.token_hex(32)


login_manager = LoginManager()

@login_manager.user_loader
def load_user(username):
    try:
        user = users_credentials.find_one({"username": username})
        if user:
            return User(username=user["username"])
        return None
    except Exception as e:
        logging.error(f"An error occurred while loading the user: {e}")
        return None

def init_login_manager(app):
    login_manager.init_app(app)
    login_manager.login_view = "ratespotter_blueprint.login"

class User(UserMixin):
    def __init__(self, username):
        self.username = username

    def get_id(self):
        return self.username



