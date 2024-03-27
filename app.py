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


# Task - User Model | id, username, password
# Sign Up page
# Login page
# Create a user, delete, update
# sign up = check if user exists
# login = check if user and password match
class User(db.Model):
    __tablename__ = "users"
    # automatically creates and assigns value
    id = db.Column(db.String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(50))
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


# Go to login page
@app.route("/login")  # HOF
def login_page():
    return render_template("login.html")


# Go to signup page
@app.route("/signup")  # HOF
def signup_page():
    return render_template("signup.html")


@app.route("/user", methods=["POST"])  # HOF
def dashboard_page():
    # have to get values from form via keys
    username = request.form.get("username")
    password = request.form.get("password")
    print("Dashboard page", username, password)
    return f"<h1>Hi {username}, welcome to our Movies App 🙂</h1>"


# Delete a user from FORM
@app.route("user/delete", methods=["POST"])
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
