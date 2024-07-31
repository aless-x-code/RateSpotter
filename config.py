from pathlib import Path
from flask import Flask
from dotenv import load_dotenv


from auth import init_login_manager, flask_secret_key
from routes import ratespotter_blueprint


current_file = Path(__file__).resolve()
app_dir = current_file.parent
static_folder = app_dir / "static"
template_folder = app_dir / "templates"


app = Flask(__name__, static_folder=static_folder, template_folder=template_folder)
load_dotenv()
app.secret_key = flask_secret_key



app.register_blueprint(ratespotter_blueprint)
init_login_manager(app)

