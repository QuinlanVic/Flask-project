from flask import Flask, jsonify, request, render_template, flash

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text

import os
from dotenv import load_dotenv
from pprint import pprint
import uuid

from extensions import db

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

db.init_app(app)
# ORM = Object Relation Mapping
# Sqlalchemy is a Python SQL toolkit & an ORM driver ->
# easy to submit SQL queries as well as map objects to table definitions and vice versa
# db = SQLAlchemy(app)  # ORM
# 3 advantages of working with the ORM driver
# can read from/work with multiple databases (just change connection string)
# no raw sql -> autocomplete functions (.get(), .all(), .filterby()) (NOT "SELECT * movies..." in string format, it's an abstraction of that)
# allows us to manipulate easier to work with datatypes (NOT query strings like above)


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
