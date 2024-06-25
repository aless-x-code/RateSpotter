from flask import render_template, request, redirect, url_for, flash, Blueprint
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from auth import login_manager, users_credentials, User, client
from scripts.database import get_tripadvisor_collection
from scripts.utilities.search import search_restaurants, get_restaurant_by_id

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
        restaurant_name = request.form["restaurant_name"]
        restaurant_zip_code = request.form["restaurant_zip_code"]

        matching_restaurants = search_restaurants(restaurant_name=restaurant_name, restaurant_zip_code=restaurant_zip_code)

        if matching_restaurants:
            return render_template('confirm_restaurant.html', matching_restaurants=matching_restaurants)
        else:
            flash('No matching restaurants found. Please try again.', 'danger')
            return redirect(url_for('ratespotter_blueprint.register'))
        
    return render_template('register.html')

@ratespotter_blueprint.route('/confirm_restaurant', methods=['POST'])
def confirm_restaurant():
    if request.method == 'POST':
        location_id = request.form["selected_restaurant"]

        selected_restaurant = get_restaurant_by_id(location_id)

        return render_template('complete_registration.html', restaurant=selected_restaurant)

    return redirect(url_for('ratespotter_blueprint.register'))


@ratespotter_blueprint.route('/complete_registration', methods=['POST'])
def complete_registration():
    if request.method == 'POST':
        username = request.form["username"]
        password = request.form["password"]
        hashed_password = generate_password_hash(password)
        restaurant_id = request.form["restaurant_id"]

        if users_credentials.find_one({'username': username}):
            flash('Username already exists. Choose a different one.', 'danger')
        elif users_credentials.find_one({'restaurant_id': restaurant_id}):
            flash('Restaurant is already linked to another account.', 'danger')
        else:
            users_credentials.insert_one({
                'username': username,
                'password': hashed_password,
                'restaurant_id': restaurant_id
            })
            flash('Registration successful. You can now log in.', 'success')
            return redirect(url_for('ratespotter_blueprint.login'))

    return redirect(url_for('ratespotter_blueprint.register'))


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

    auth_db = client.auth
    users_credentials = auth_db.user_credentials
    user = users_credentials.find_one({'username': current_user.username})
    restaurant_id = user.get('restaurant_id')
    tripadvisor_reviews = get_tripadvisor_collection(restaurant_id)

    restaurant_name = get_restaurant_by_id(restaurant_id)["name"]


    if tripadvisor_reviews is not None:
        return render_template("user_homepage.html", username=current_user.username, tripadvisor_reviews=tripadvisor_reviews, restaurant_name=restaurant_name)
    else:
        flash('Error accessing your data.', 'danger')
        return redirect(url_for('ratespotter_blueprint.login'))

    


