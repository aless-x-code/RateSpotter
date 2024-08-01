from flask import render_template, request, redirect, url_for, flash, Blueprint, session
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import logging

from auth import users_credentials, User, mongo_client
from scripts.reviews import get_tripadvisor_id, get_google_id, get_yelp_id
from scripts.utilities import search_restaurants
from ReviewManager import ReviewManager

ratespotter_blueprint = Blueprint("ratespotter_blueprint", __name__)

logging.basicConfig(level=logging.ERROR)


@ratespotter_blueprint.route("/")
def index():
    try:
        return render_template("index.html")
    except Exception as e:
        logging.error(f"Template not found: {e}")
        return f"Template not found: {e}"


@ratespotter_blueprint.route('/find_restaurant', methods=['GET', 'POST'])
def find_restaurant():
    if request.method == 'POST':
        try: 
            restaurant_name = request.form["restaurant_name"]
            restaurant_zip = request.form["restaurant_zip"]

            matching_restaurants = search_restaurants(restaurant_name, restaurant_zip)

            if matching_restaurants:
                return render_template('select_restaurant.html', matching_restaurants=matching_restaurants)
            else:
                flash('No matching restaurants found. Please try again.', 'failure')
                return redirect(url_for('ratespotter_blueprint.find_restaurant'))
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
            flash('An error occurred while processing your request. Please try again.', 'failure')
            return redirect(url_for('ratespotter_blueprint.find_restaurant'))
        
    return render_template('find_restaurant.html')

@ratespotter_blueprint.route('/select_restaurant', methods=['POST'])
def select_restaurant():
    if request.method == 'POST':
        try:
            selected_restaurant_id = request.form["selected_restaurant_id"]
            selected_restaurant_name = request.form["selected_restaurant_name"]
            selected_restaurant_address = request.form["selected_restaurant_address"]

            return render_template('complete_registration.html', 
                                   selected_restaurant_id=selected_restaurant_id, selected_restaurant_name=selected_restaurant_name, selected_restaurant_address=selected_restaurant_address)
        
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
            flash('An error occurred while processing your request. Please try again.', 'failure')
            return redirect(url_for('ratespotter_blueprint.find_restaurant'))
        
    return redirect(url_for('ratespotter_blueprint.find_restaurant'))


@ratespotter_blueprint.route('/complete_registration', methods=['POST'])
def complete_registration():
    if request.method == 'POST':
        try: 
            username = request.form["username"]
            password = request.form["password"]

            selected_restaurant_id = request.form["selected_restaurant_id"]
            selected_restaurant_name = request.form["selected_restaurant_name"]
            selected_restaurant_address = request.form["selected_restaurant_address"]

            if users_credentials.find_one({'username': username}):
                flash('Username already exists. Choose a different one.', 'failure')
                return render_template('complete_registration.html', 
                                    selected_restaurant_id=selected_restaurant_id, selected_restaurant_name=selected_restaurant_name, selected_restaurant_address=selected_restaurant_address)
            elif users_credentials.find_one({'restaurant_name': selected_restaurant_name}):
                flash('Restaurant is already linked to another account.', 'failure')
            else:
                hashed_password = generate_password_hash(password)
                tripadvisor_id = get_tripadvisor_id(selected_restaurant_name, selected_restaurant_address)
                # yelp_id = get_yelp_id(selected_restaurant_name, selected_restaurant_address)
                # google_id = get_google_id(selected_restaurant_name, selected_restaurant_address)

                users_credentials.insert_one({
                    'username': username,
                    'password': hashed_password,
                    'restaurant_id': selected_restaurant_id,
                    'tripadvisor_id': tripadvisor_id,
                    # 'yelp_id': yelp_id,
                    # 'google_id': google_id,
                    'restaurant_name': selected_restaurant_name,
                    'restaurant_address': selected_restaurant_address
                })
                flash('Registration successful. You can now log in.', 'success')
                return render_template('login.html', username=username)
            
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
            flash('An error occurred while processing your request. Please try again.', 'failure')
            return redirect(url_for('ratespotter_blueprint.find_restaurant'))

    return redirect(url_for('ratespotter_blueprint.find_restaurant'))


@ratespotter_blueprint.route('/login', methods=['GET', 'POST'])
def login():    
    if request.method == 'POST':
        try: 
            username = request.form['username']
            password = request.form['password']
            user = users_credentials.find_one({'username': username})

            if user and check_password_hash(user['password'], password):
                user_obj = User(username=user['username'])
                login_user(user_obj)
                flash('Login successful.', 'success')
                return redirect(url_for('ratespotter_blueprint.user_homepage'))
            else:
                flash('Invalid username or password. Please try again.', 'failure')
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
            flash('An error occurred while processing your request. Please try again.', 'failure')
            return redirect(url_for('ratespotter_blueprint.login'))

    return render_template('login.html')

cache = {}
@ratespotter_blueprint.route('/user_homepage')
@login_required
def user_homepage():
    try:
        user = users_credentials.find_one({'username': current_user.username})
        username = current_user.username
        restaurant_name = user.get('restaurant_name')

        user_reviews = mongo_client["user_reviews"] 
        review_collection = user_reviews[f"{username}_review_collection"]

        if username not in cache:
            # cache[username] = [ReviewManager('tripadvisor', review_collection), 
            #                    ReviewManager('google', review_collection), 
            #                    ReviewManager('yelp', review_collection)]
            cache[username] = [ReviewManager('tripadvisor', review_collection)]

        review_managers = cache[username]
    
        return render_template("user_homepage.html", 
                            username=username, 
                            restaurant_name=restaurant_name,  
                            review_managers=review_managers,
                            review_managers_len=len(review_managers)
                            )
    except Exception as e:
            logging.error(f"An unexpected error occurred while loading user homepage: {e}")
            flash('An error occurred while processing your request. Please try again.', 'failure')
            return redirect(url_for('ratespotter_blueprint.logout'))


@ratespotter_blueprint.route('/logout')
@login_required
def logout():
    if current_user.username in cache:
        del cache[current_user.username]
    session.clear()
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('ratespotter_blueprint.login'))


@ratespotter_blueprint.context_processor
def utility_processor():
    def generate_stars(rating):
        try:
            star_emoji = '\u2B50'
            return star_emoji * int(rating)
        except Exception as e:
            logging.error(f"An unexpected error occurred while generating stars for rating: {e}")
            flash('An error occurred while processing your request. Please try again.', 'failure')
            return redirect(url_for('ratespotter_blueprint.logout'))
    
    def generate_void_stars(rating):
        try:
            void_star_emoji = '\u2606'
            return void_star_emoji * (5 - int(rating)) 
        except Exception as e:
            logging.error(f"An unexpected error occurred while generatin empty stars for rating: {e}")
            flash('An error occurred while processing your request. Please try again.', 'failure')
            return redirect(url_for('ratespotter_blueprint.logout'))
    
    return dict(generate_stars=generate_stars, generate_void_stars=generate_void_stars)
   




