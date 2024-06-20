# from flask import Blueprint
# from auth import User, users_collection
# from flask_login import login_user, login_required, logout_user, current_user
# from werkzeug.security import generate_password_hash, check_password_hash
# from flask import Flask, render_template, request, redirect, url_for, flash

# movies_api_v1 = Blueprint("ratespotter_blueprint", __name__)

# @movies_api_v1.route("/")
# def index():
#     return render_template("index.html")

# @movies_api_v1.route('/register', methods=['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         hashed_password = generate_password_hash(password)

#         if users_collection.find_one({'username': username}):
#             flash('Username already exists. Choose a different one.', 'danger')
#         else:
#             users_collection.insert_one({'username': username, 'password': hashed_password})
#             flash('Registration successful. You can now log in.', 'success')
#             return redirect(url_for('ratespotter_blueprint.login'))

#     return render_template('register.html')

# @movies_api_v1.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         user = users_collection.find_one({'username': username})

#         if user and check_password_hash(user['password'], password):
#             user_obj = User(username=user['username'])
#             login_user(user_obj)
#             flash('Login successful.', 'success')
#             return redirect(url_for('ratespotter_blueprint.user_homepage'))
#         else:
#             flash('Invalid username or password. Please try again.', 'danger')

#     return render_template('login.html')

# @movies_api_v1.route('/logout')
# @login_required
# def logout():
#     logout_user()
#     flash('You have been logged out.', 'success')
#     return redirect(url_for('ratespotter_blueprint.login'))

# @movies_api_v1.route('/user_homepage')
# @login_required
# def user_homepage():
#     return render_template("user_homepage.html", username=current_user.username)
