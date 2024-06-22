import os
from dotenv import load_dotenv
from flask_login import LoginManager, UserMixin 
from pymongo.mongo_client import MongoClient 
from pymongo.server_api import ServerApi 
import certifi

def init_login_manager(app):
    login_manager.init_app(app)
    login_manager.login_view = "ratespotter_blueprint.login"

class User(UserMixin):
    def __init__(self, username):
        self.username = username

    def get_id(self):
        return self.username

load_dotenv()

mongo_pw = os.environ.get("mongo_pw")
mongo_user = os.environ.get("mongo_user")

uri = f"mongodb+srv://{mongo_user}:{mongo_pw}@ratespotter-cluster.k6gug4f.mongodb.net/?retryWrites=true&w=majority&appName=ratespotter-cluster"
mongodb_client = MongoClient(uri, server_api=ServerApi('1'), tlsCAFile=certifi.where())
auth_db = mongodb_client[os.environ.get("auth_db")] 
users_credentials = auth_db[os.environ.get("user_credentials")]

login_manager = LoginManager()



