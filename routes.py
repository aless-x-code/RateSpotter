from flask import render_template, request, redirect, url_for, flash, Blueprint
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from auth import login_manager, users_credentials, User
from scripts.database import get_tripadvisor_collection

ratespotter_blueprint = Blueprint("ratespotter_blueprint", __name__)
    
@login_manager.user_loader
def load_user(username):
    user = users_credentials.find_one({"username": username})
    if user:
        return User(username=user["username"])
    return None

@ratespotter_blueprint.route("/")
def index():
    return render_template("index.html")

@ratespotter_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)

        if users_credentials.find_one({'username': username}):
            flash('Username already exists. Choose a different one.', 'danger')
        else:
            users_credentials.insert_one({'username': username, 'password': hashed_password})
            flash('Registration successful. You can now log in.', 'success')
            return redirect(url_for('ratespotter_blueprint.login'))

    return render_template('register.html')

@ratespotter_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = users_credentials.find_one({'username': username})

        if user and check_password_hash(user['password'], password):
            user_obj = User(username=user['username'])
            login_user(user_obj)
            flash('Login successful.', 'success')
            return redirect(url_for('ratespotter_blueprint.user_homepage'))
        else:
            flash('Invalid username or password. Please try again.', 'danger')

    return render_template('login.html')

@ratespotter_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('ratespotter_blueprint.login'))

@ratespotter_blueprint.route('/user_homepage')
@login_required
def user_homepage():
    return render_template("user_homepage.html", username=current_user.username, tripadvisor_reviews=get_tripadvisor_collection())


