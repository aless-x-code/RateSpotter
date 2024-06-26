import os
from pathlib import Path
from flask import Flask
from dotenv import load_dotenv
import secrets


from auth import init_login_manager
from routes import ratespotter_blueprint

# client.close() ??
# try exception
# improve library function parameters
# @media css
# modern css practices
# GET methods for confirm_restaurant/confirm?


current_file = Path(__file__).resolve()
app_dir = current_file.parent
static_folder = app_dir / "static"
template_folder = app_dir / "templates"

app = Flask(__name__, static_folder=static_folder, template_folder=template_folder)

load_dotenv()
app.secret_key = os.environ.get("FLASK_SECRET_KEY") or secrets.token_hex(32)

app.register_blueprint(ratespotter_blueprint)
init_login_manager(app)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
