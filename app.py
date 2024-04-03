from flask import Flask, jsonify, request, render_template, flash

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text

import os
from dotenv import load_dotenv
from pprint import pprint
import uuid

from flask_wtf import FlaskForm

import json

# All to keep away private passwords and stuff away from the public via
# puts variables in .env file into windows environmental variables
load_dotenv()  # load -> os env (environmental variables)
# print(os.environ.get("AZURE_DATABASE_URL"))


# create an instance of the 'Flask' class
app = Flask(__name__)

# secret so we have to provide it in the ".env" file
app.config["SECRET_KEY"] = os.environ.get("FORM_SECRET_KEY")  # token

# General Pattern
# mssql+pyodbc://<username>:<password>@<dsn_name>?driver=<driver_name>

# connect to our azure
# change connection string when working with different databases
connection_string = os.environ.get("AZURE_DATABASE_URL")
app.config["SQLALCHEMY_DATABASE_URI"] = connection_string
# ORM = Object Relation Mapping
# Sqlalchemy is a Python SQL toolkit & an ORM driver ->
# easy to submit SQL queries as well as map objects to table definitions and vice versa
db = SQLAlchemy(app)  # ORM
# 3 advantages of working with the ORM driver
# can read from/work with multiple databases (just change connection string)
# no raw sql -> autocomplete functions (.get(), .all(), .filterby()) (NOT "SELECT * movies..." in string format, it's an abstraction of that)
# allows us to manipulate easier to work with datatypes (NOT query strings like above)


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


class User(db.Model):
    __tablename__ = "users"
    # automatically creates and assigns value
    id = db.Column(db.String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
    # make unique
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    # JSON - Keys (can change names sent to front-end)
    # class method
    # dict is also easier to convert to JSON
    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password,
        }


# to test connection
try:
    with app.app_context():
        # Use text() to explicitly declare your SQL command
        result = db.session.execute(text("SELECT 1")).fetchall()
        print("Connection successful:", result)
        # only use create all once and then comment out again so it doesn't try to create tables with each restart of the server
        # it won't cause an error as it only adds if it doesn't exist
        # but always keep it there when in production (for updates)
        # db.create_all()  # easier way to create tables through python after connecting
except Exception as e:
    print("Error connecting to the database:", e)

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


# have to have import here because by now the db would have been created and movies_bp can import it from app
from main_bp import main_bp

# registering "main_bp.py" as a blueprint
# view (Python fullstack) -> actually implementing through forms and stuff
app.register_blueprint(main_bp)


from about_bp import about_bp


# registering "about_bp.py" as a blueprint and add a prefix for the url
app.register_blueprint(about_bp, url_prefix="/about")


from user_bp import user_bp

# registering "user_bp.py" as a blueprint
# view (Python fullstack) -> actually implementing through forms and stuff
app.register_blueprint(user_bp)


# store tokens in browser (local storage or cookies) (gets given after signing up/logging in)
# no token, no data
