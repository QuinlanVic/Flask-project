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


# have to have import here because by now the db would have been created and movies_bp can import it from app
# from user_bp import user_bp

# registering "user_bp.py" as a blueprint and add a prefix for the url
# view (Python fullstack) -> actually implementing through forms and stuff
# app.register_blueprint(user_bp, url_prefix="/user")


from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError


# registration validation
class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=6)])
    password = PasswordField(
        "Password", validators=[InputRequired(), Length(min=8, max=12)]
    )
    submit = SubmitField("Sign Up")

    # use WTF to send user back to registration page if input is invalid
    # automatically runs when the "form.validate_on_submit()" function executes
    # class method (instance and data from user form via field)
    # validate = function name and then "_" then the field name
    def validate_username(self, field):
        # inform WTF that there is an error and display it
        print("Validate username was called (reg)", field.data)
        specific_user = User.query.filter_by(username=field.data).first()
        # print(specific_user)

        # if it does exist then user cannot sign up and send them back to register page
        if specific_user:
            # the message below is displayed in the "div" in the register form
            raise ValidationError("Username taken")


# login validation
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    submit = SubmitField("Login")

    # validate = function name and then "_" then the field name
    def validate_username(self, field):
        # inform WTF that there is an error and display it
        print("Validate username was called (log)", field.data)
        specific_user = User.query.filter_by(username=field.data).first()
        # print(specific_user)

        # if it does not exist then user cannot log in and we send them back to getin page
        if not specific_user:
            # the message below is displayed in the "div" in the register form
            raise ValidationError("Username or password invalid")

    # Validate for login form
    def validate_password(self, field):
        # access username via self
        user = User.query.filter_by(username=self.username.data).first()
        if user:
            if user.password != field.data:
                raise ValidationError("Username or password is invalid")


# GET - Issue token
# POST - Verify token
# new route for register page
@app.route("/getin", methods=["GET", "POST"])  # HOF
def getin_page():
    # GET & POST
    # create a new form object
    form = LoginForm()

    # only on POST (when user is registering)
    if form.validate_on_submit():
        # check if username is already in database
        # specific_user = User.query.get(form.username.data)
        # specific_user = db.session.query(User).filter(
        #     User.username == (form.username.data)
        # )
        # or
        specific_user = User.query.filter_by(username=form.username.data).first()
        print(specific_user)

        # if it does not exist then user cannot sign up and send them back to register page
        if not specific_user or specific_user.password != form.password.data:
            # flash("Invalid username or password", "danger")
            return render_template("getin.html", form=form)
        # otherwise user has logged in successfully
        return f"<h1>Welcome back, {form.username.data}"

    # only on GET
    # then use it in register page
    return render_template("getin.html", form=form)


# GET - Issue token
# POST - Verify token
# new route for register page
@app.route("/register", methods=["GET", "POST"])  # HOF
def register_page():
    # GET & POST
    # create a new form object
    form = RegistrationForm()

    # only on POST (when user is registering)
    if form.validate_on_submit():
        # check if username is already in database
        # specific_user = User.query.get(form.username.data)
        # specific_user = db.session.query(User).filter(
        #     User.username == (form.username.data)
        # )
        # or
        specific_user = User.query.filter_by(username=form.username.data).first()
        print(specific_user)

        # if it does exist then user cannot sign up and send them back to register page
        if specific_user:
            return render_template("register.html", form=form)
        # otherwise create a new user entry
        # print(form.username.data, form.password.data)
        # add registered users to the database
        new_user = User(
            username=form.username.data, password=form.password.data
        )  # id should be auto-created
        try:
            db.session.add(new_user)
            db.session.commit()
            # print("Profile page", username, password)
            return "<h1> Registration successful </h1>", 201
        # now send them to new profile page
        # return render_template("profile.html", new_user.to_dict())
        except Exception as e:
            db.session.rollback()  # undo the change (unless committed already)
            return f"<h1>An error occured: {str(e)}", 500

    # only on GET
    # then use it in register page
    return render_template("register.html", form=form)


# store tokens in browser (local storage or cookies) (gets given after signing up/logging in)
# no token, no data
