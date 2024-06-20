# from flask import Flask
# from flask_login import LoginManager, UserMixin #type: ignore
# from werkzeug.security import generate_password_hash, check_password_hash
# import os
# from pymongo.mongo_client import MongoClient #type: ignore
# from pymongo.server_api import ServerApi #type: ignore
# import certifi
# from dotenv import load_dotenv

# load_dotenv()

# mongo_db_pw = os.environ.get("mongo_db_pw")
# mongo_user = os.environ.get("mongo_user")

# uri = f"mongodb+srv://{mongo_user}:{mongo_db_pw}@test-db.rzdnkbr.mongodb.net/?retryWrites=true&w=majority&appName=test-db"
# client = MongoClient(uri, server_api=ServerApi('1'), tlsCAFile=certifi.where())
# db = client[os.environ.get("db_name")] 
# users_collection = db[os.environ.get("collection")]

# login_manager = LoginManager()

# class User(UserMixin):
#     def __init__(self, username):
#         self.username = username

#     def get_id(self):
#         return self.username

# @login_manager.user_loader
# def load_user(username):
#     user = users_collection.find_one({"username": username})
#     if user:
#         return User(username=user["username"])
#     return None

# def init_login_manager(app):
#     login_manager.init_app(app)
#     login_manager.login_view = "ratespotter_blueprint.login"
