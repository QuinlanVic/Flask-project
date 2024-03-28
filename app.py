from flask import Flask, jsonify, request, render_template

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text

import os
from dotenv import load_dotenv
from pprint import pprint
import uuid


import json

# All to keep away private passwords and stuff away from the public via
# puts variables in .env file into windows environmental variables
load_dotenv()  # load -> os env (environmental variables)
# print(os.environ.get("AZURE_DATABASE_URL"))


# create an instance of the 'Flask' class
app = Flask(__name__)

# General Pattern
# mssql+pyodbc://<username>:<password>@<dsn_name>?driver=<driver_name>

# connect to our azure
# change connection string when working with different databases
connection_string = os.environ.get("AZURE_DATABASE_URL")
app.config["SQLALCHEMY_DATABASE_URI"] = connection_string
db = SQLAlchemy(app)  # ORM
# 3 advantages of working with the ORM driver
# can read from/work with multiple databases (just change connection string)
# no raw sql -> autocomplete functions (NOT "SELECT * movies..." in string format)
# allows us to manipulate easier to work with datatypes (NOT query strings like above)

# to test connection
try:
    with app.app_context():
        # Use text() to explicitly declare your SQL command
        result = db.session.execute(text("SELECT 1")).fetchall()
        print("Connection successful:", result)
except Exception as e:
    print("Error connecting to the database:", e)


# Model (SQLAlchemy) == Schema
# CREATE TABLE movies (
# 	has to be varchar so it can be indexed for increased performance (TEXT cannot be indexed)
# 	id VARCHAR(50) PRIMARY KEY,
# 	name VARCHAR(100),
# 	poster VARCHAR(255),
# 	rating FLOAT,
# 	summary VARchAR(500),
# 	trailer VARCHAR(255)
# )


# schema for the table
# constructor we are using is from "db.Model"
class Movie(db.Model):
    __tablename__ = "movies"
    # automatically creates and assigns value
    # increased performance if you do not do calculations to update id by max id on the python side
    # if autoincremented on the SQL side it will not have a decrease in preformance as it will remember the last value and update easily
    # increased security as it is more difficult for people to guess "id" values
    # easier to merge two tables as their id primary keys will not be the same/consist of duplicates
    id = db.Column(db.String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(50))
    poster = db.Column(db.String(50))
    rating = db.Column(db.Float(50))
    summary = db.Column(db.String(50))
    trailer = db.Column(db.String(50))

    # JSON - Keys (can change names sent to front-end)
    # class method
    # dict is also easier to convert to JSON
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "poster": self.poster,
            "rating": self.rating,
            "summary": self.summary,
            "trailer": self.trailer,
        }


# have to have import here because by now the db would have been created and movies_bp can import it from app
from movies_bp import movies_bp

# registering "movies_bp.py" as a blueprint and add a prefix for the url
# JSON (For front-end people)
app.register_blueprint(movies_bp, url_prefix="/movies")

# have to have import here because by now the db would have been created and movies_bp can import it from app
from movieslist_bp import movieslist_bp

# registering "movieslist_bp.py" as a blueprint and add a prefix for the url
# view (Python fullstack) -> actually implementing through forms and stuff
app.register_blueprint(movieslist_bp, url_prefix="/movieslist")


# ***************************************** EVERYTHING BESIDES MOVIES *********************************************


# home page
@app.route("/")  # HOF (Higher Order Function)
def hello_world():
    return "<h1>Super, Cool 😁</h1>"


name = "Caleb"
hobbies = ["Gaming", "Reading", "Soccer", "Ballet", "Gyming"]


from about_bp import about_bp


# registering "about_bp.py" as a blueprint and add a prefix for the url
app.register_blueprint(about_bp, url_prefix="/about")


# /profile page
@app.route("/profile")
def profile_page():
    return render_template("profile.html", name=name, hobbies=hobbies)


@app.route("/sample")
def sample_page():
    return render_template("sample.html")


# Task - User Model | id, username, password
# Sign Up page
# Login page
# Create a user, delete, update, get
# sign up = check if user exists
# login = check if user and password match
class User(db.Model):
    __tablename__ = "users"
    # automatically creates and assigns value
    id = db.Column(db.String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    # make unique
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))

    # JSON - Keys (can change names sent to front-end)
    # class method
    # dict is also easier to convert to JSON
    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password,
        }


# have to have import here because by now the db would have been created and movies_bp can import it from app
# from user_bp import user_bp

# registering "user_bp.py" as a blueprint and add a prefix for the url
# view (Python fullstack) -> actually implementing through forms and stuff
# app.register_blueprint(user_bp, url_prefix="/user")


# Go to login page
@app.route("/login")  # HOF
def login_page():
    return render_template("login.html")


# Go to signup page
@app.route("/signup")  # HOF
def signup_page():
    return render_template("signup.html")


# log a user in
@app.route("/user", methods=["POST"])  # HOF
def dashboard_page():
    # have to get values from form via keys
    username = request.form.get("username")
    password = request.form.get("password")
    # check if username and password match
    specific_user = User.query.get(username)
    # if the username or password is incorrect they cannot log in
    if not specific_user or specific_user.password != password:
        return f"<h1>Username or password is incorrect, please try again :)</h1>"
    # otherwise log the user in
    print("Dashboard page", username, password)
    return f"<h1>Hi {username}, welcome back to our Movies App 🙂</h1>"


# get a user by id
# specific movie page
@movieslist_bp.route("/user/<id>")
def profile_page(id):
    specific_user = User.query.get(id)
    if specific_user is None:
        return "<h1>User not found</h1>"
    return render_template("profile.html", movie=specific_user.to_dict())


# sign a user up
@app.route("/user/profile", methods=["POST"])  # HOF
def profile_page():
    # have to get values from form via keys
    username = request.form.get("username")
    password = request.form.get("password")
    # check if username is already in database
    specific_user = User.query.get(username)
    # if it does exist then user cannot sign up
    if specific_user:
        return f"<h1>User already exists, please input a different username :)</h1>"
    # otherwise create a new user entry
    new_user = User(username=username, password=password)  # id should be auto-created
    try:
        db.session.add(new_user)
        db.session.commit()
        print("Profile page", username, password)
        # now send them to new profile page
        # return f"<h1>Hi {username}, welcome to our Movies App 🙂</h1>"
        return render_template("profile.html", new_user.to_dict())
    except Exception as e:
        db.session.rollback()  # undo the change (unless committed already)
        return f"<h1>An error occured: {str(e)}", 500


# Delete a user from FORM
@app.route("/user/delete", methods=["POST"])
def delete_user_by_id():
    id = request.form.get("user_id")
    user = User.query.get(id)

    # if user is not found
    if not user:
        return "<h1>User not found</h1>", 404

    # otherwise delete it
    try:
        db.session.delete(user)
        db.session.commit()
        return f"<h1>{user.username} successfully deleted"
    except Exception as e:
        return f"<h1>An error occured: {str(e)}</h1>", 500


# update user form route
# Task - /user/update -> Update user form (2 existing fields = username and password) -> Submit -> /users
# Has to be post to pass the data for some reason?
# take you to update form with data after manipulation
@movieslist_bp.route("/user/update", methods=["POST"])
def update_user_page():
    user = request.form.get("user")
    print(user)
    print(type(user))
    # funny error as JSON only supports single quotes LOLOLOLOLOL
    user_json = user.replace("'", '"')
    # convert into a dict
    user_dict = json.loads(user_json)
    print(type(user_dict))
    return render_template("updateuser.html", movie=user_dict)


# UPDATE USER FORM TO SQL DATABASE
# has to be a different url or it will do the other "/update" above as
# it also uses a POST method because it has to for passing data for some reason
@movieslist_bp.route("/user/update/db", methods=["POST"])
def update_user_list():
    user_id = request.form.get("id")
    update_data = {
        "username": request.form.get("username"),
        "password": request.form.get("password"),
    }
    specific_user = User.query.get(user_id)
    if specific_user is None:
        return "<h1>User not found</h1>"
    try:
        # update all values in "specific_user" with values from "update_data" dictionary
        # loop body as you only want to work with specific keys we need to update
        for key, value in update_data.items():
            # if they put in random keys it will change it which is unsafe!!!!
            # specific_user.key = update_data.get(key, specific_user.key)
            # so now we check if the key is in the table and only work with it if it is
            if hasattr(specific_user, key):
                # now update those values
                setattr(specific_user, key, value)
        db.session.commit()
        return f"{specific_user.username} successfully updated"
    except Exception as e:
        return f"<h1>An error occured: {str(e)}"
