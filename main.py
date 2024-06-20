import os
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv
import secrets
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin #type: ignore
from pymongo.mongo_client import MongoClient #type: ignore
from pymongo.server_api import ServerApi #type: ignore
import certifi
from routes import init_login_manager
from routes import movies_api_v1


load_dotenv()

current_file = Path(__file__).resolve()
app_dir = current_file.parent
static_folder = app_dir / "static"
template_folder = app_dir / "templates"

app = Flask(__name__, static_folder=static_folder, template_folder=template_folder)
app.secret_key = os.environ.get("FLASK_SECRET_KEY") or secrets.token_hex(32)

app.register_blueprint(movies_api_v1)
init_login_manager(app)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
