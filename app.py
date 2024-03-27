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

# change connection string when working with different databases
connection_string = os.environ.get("AZURE_DATABASE_URL")
app.config["SQLALCHEMY_DATABASE_URI"] = connection_string
db = SQLAlchemy(app)  # ORM
# 3 advantages of working with the ORM driver
# can read from/work with multiple databases (just change connection string)
# no raw sql -> autocomplete functions (NOT "SELECT * movies..." in string format)
# allows us to work with easier to work with datatypes (NOT query strings like above)

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


# connect to our azure
# constructor we are using is from "db.Model"
class Movie(db.Model):
    __tablename__ = "movies"
    # automatically creates and assigned value
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


from movies_bp import movies_bp

# registering "about_bp.py" as a blueprint and add a prefix for the url
app.register_blueprint(movies_bp, url_prefix="/movies")


# Task 2 - get movies from database
# movies list
@app.route("/movieslist")
def movie_list_page():
    movie_list = Movie.query.all()  # SELECT * FROM movies | movie_list iterator
    # print(type(movie_list)) # list
    # print(type(movie_list[0])) # app.Movie
    data = [movie.to_dict() for movie in movie_list]  # convert to a list of dict
    return render_template("movies-list.html", movies=data)


# Task 3 - display the data for specific movie on page
# specific movie page
@app.route("/movieslist/<id>")
def movie_page(id):
    specific_movie = Movie.query.get(id)

    if specific_movie is None:
        return "<h1>Movie not found</h1>"

    return render_template("movie.html", movie=specific_movie.to_dict())


@app.route("/movielist/delete", methods=["POST"])
def delete_movie_by_id():
    id = request.form.get("movie_id")
    movie = Movie.query.get(id)
    # print(request.form.get("movie_id")) # test if we found the correct id value
    # movie = Movie.query.get(id)
    if not movie:
        # return jsonify({"message": "Movie not found"}), 404
        # Do not return JSON data as you want to display the information on the screen
        return "<h1>Movie not found</h1>", 404
    # otherwise delete it
    try:
        db.session.delete(movie)
        db.session.commit()
        # return jsonify({"message": "Movie deleted successfully", "data": movie.to_dict()})
        # Do not return JSON data as you want to display the information on the screen
        return f"<h1>{movie.to_dict()['name']} successfully deleted</h1>"
    except Exception as e:
        # return jsonify({"error": str(e)})
        # Do not return JSON data as you want to display the information on the screen to the user
        return f"<h1>An error occured: {str(e)}</h1>", 500


# ADD MOVIE TO SQL DATABASE NOW NOT LOCAL
@app.route("/movieslist", methods=["POST"])
def new_movie_list():
    movie_name = request.form.get("name")
    movie_poster = request.form.get("poster")
    movie_rating = request.form.get("rating")
    movie_summary = request.form.get("summary")
    movie_trailer = request.form.get("trailer")
    # create new movie
    new_movie = Movie(
        name=movie_name,
        poster=movie_poster,
        rating=movie_rating,
        summary=movie_summary,
        trailer=movie_trailer,
    )
    try:
        db.session.add(new_movie)
        db.session.commit()
        movie_list = Movie.query.all()
        data = [movie.to_dict() for movie in movie_list]  # convert to a list of dict
        # return render_template("movies-list.html", movies=data)
        return f"{new_movie.name} successfully created"
    except Exception as e:
        db.session.rollback()  # Undo the change (cannot be done if already committed)
        return f"<h1>An error occured: {str(e)}", 500


# UPDATE MOVIE FORM TO SQL DATABASE NOW NOT LOCAL
@app.route("/movieslist", methods=["POST"])
def update_movie_list():
    movie_name = request.form.get("name")
    movie_poster = request.form.get("poster")
    movie_rating = request.form.get("rating")
    movie_summary = request.form.get("summary")
    movie_trailer = request.form.get("trailer")
    update_data = {
        "name": movie_name,
        "poster": movie_poster,
        "rating": movie_rating,
        "summary": movie_summary,
        "trailer": movie_trailer,
    }
    specific_movie = Movie.query.get(id)
    if specific_movie is None:
        result = {"message": "movie not foumd"}
        return "<h1>Movie not found</h1>"
    try:
        # update all values in "specific_movie" with values from "update_data" dictionary
        # loop body as you only want to work with specific keys we need to update
        for key, value in update_data.items():
            # if they put in random keys it will change it which is unsafe!!!!
            # specific_movie.key = update_data.get(key, specific_movie.key)
            # so now we check if the key is in the table and only work with it if it is
            if hasattr(specific_movie, key):
                # now update those values
                setattr(specific_movie, key, value)
        db.session.commit()
        return f"{specific_movie.name} successfully created"
    except Exception as e:
        return f"<h1>An error occured: {str(e)}"


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


# /dashboard page (OLD)
# @app.route("/dashboard2")
# def dashboard_page2():
#     return render_template("dashboard2.html", movies=movies)


# movies list
# @app.route("/movieslist")
# def movie_list_page():
#     return render_template("movies-list.html", movies=movies)


# specific movie page
# @app.route("/movieslist/<id>")
# def movie_page(id):
# movie = get_specific_movie(id)
# specific_movie = next((movie for movie in movies if movie["id"] == id), None)

# if specific_movie is None:
#     result = {"message": "movie not found"}
#     return "<h1>Movie not found</h1>"

# result = {"message": "movie successfully found", "data": specific_movie}
# return render_template("movie.html", movie=specific_movie)


@app.route("/login", methods=["GET"])  # HOF
def login_page():
    # How to get GET request data
    username = request.args.get("username")
    password = request.args.get("password")
    return render_template("forms.html")


@app.route("/dashboard", methods=["POST"])  # HOF
def dashboard_page():
    # have to get values from form via keys
    username = request.form.get("username")
    password = request.form.get("password")
    print("Dashboard page", username, password)
    return f"<h1>Hi {username}, welcome to our Movies App 🙂</h1>"


# Task - /movies/update -> update movie form (5 fields = name, poster, rating, summary, trailer) -> Submit -> /movies-list
# @app.route("/movies/update")
# def add_movie_page():
#     return render_template("updatemovie.html")

# @app.route("/movieslist", methods=["POST"])
# def new_movie_list():
#     movie_name = request.form.get("name")
#     movie_poster = request.form.get("poster")
#     movie_rating = request.form.get("rating")
#     movie_summary = request.form.get("summary")
#     movie_trailer = request.form.get("trailer")
#     newmovie = {
#         "name": movie_name,
#         "poster": movie_poster,
#         "rating": float(movie_rating),
#         "summary": movie_summary,
#         "trailer": movie_trailer,
#     }
#     movie_ids = [int(movie["id"]) for movie in movies]
#     max_id = max(movie_ids)
#     print(max_id)
#     # or
#     newmovie["id"] = str(max_id + 1)
#     movies.append(newmovie)
#     return render_template("movies-list.html", movies=movies)


# @app.route("/movieslist", methods=["POST"])
# def new_movie_list():
#     movie_name = request.form.get("name")
#     movie_poster = request.form.get("poster")
#     movie_rating = request.form.get("rating")
#     movie_summary = request.form.get("summary")
#     movie_trailer = request.form.get("trailer")
#     newmovie = {
#         "name": movie_name,
#         "poster": movie_poster,
#         "rating": float(movie_rating),
#         "summary": movie_summary,
#         "trailer": movie_trailer,
#     }
#     movie_ids = [int(movie["id"]) for movie in movies]
#     max_id = max(movie_ids)
#     print(max_id)
#     # or
#     newmovie["id"] = str(max_id + 1)
#     movies.append(newmovie)
#     return render_template("movies-list.html", movies=movies)


# Spider-Man 2
# https://m.media-amazon.com/images/M/MV5BMzY2ODk4NmUtOTVmNi00ZTdkLTlmOWYtMmE2OWVhNTU2OTVkXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_.jpg
# 7.5
# Peter Parker is beset with troubles in his failing personal life as he battles a former brilliant scientist named Otto Octavius.
# https://www.imdb.com/video/vi629801241/?playlistId=tt0316654&ref_=tt_pr_ov_vi


# ***************************** OLD CODE VERSION *********************************************************************************************************************

# GET -> movies page -> JSON
# @app.get("/movies")
# def get_movies():
# have to convert to JSON (using jsonify library from Flask)
# return jsonify(movies)


# POST -> request.json -> create movie + add to movies list -> JSON
# 1 more than the max id
# @app.post("/movies")
# def create_movie():
# get new movie JSON data from body in request
# new_movie = request.json
# movie_ids = [int(movie["id"]) for movie in movies]
# print(movie_ids)
# max_id = max(movie_ids)
# print(max_id)
# dictionary
# print(type(new_movie))
# new_movie = {**new_movie, "id": str(max_id + 1)}

# or
# new_movie["id"] = str(max_id + 1)
# check if movie is correctly updated with new id
# print(new_movie)
# add to movies list of dict
# movies.append(new_movie)
# create message to return
# result = {"message": "added successfully", "data": new_movie}
# added status code
# return jsonify(result), 201


# <variable_name> -> becomes the keyword argument to "get_specific_movie"
# @app.get("/movies/<id>")
# def get_specific_movie(id):
#     print(type(id))  # string
# specific_movie = [movie for movie in movies if int(movie["id"]) == int(id)]

# or - generator expression + have to account for when nothing is found (default val = None)
# specific_movie = next((movie for movie in movies if movie["id"] == id), None)
# print(type(specific_movie))

# if specific_movie == []:
# if specific_movie is None:
#     result = {"message": "movie not found"}
#     return jsonify(result), 404

# result = {"message": "movie successfully found", "data": specific_movie[0]}
# result = {"message": "movie successfully found", "data": specific_movie}
# return jsonify(result)


# create delete API for movies
# @app.delete("/movies/<id>")
# def delete_movie(id):
# movie_del = [movie for movie in movies if int(movie["id"]) == int(id)]

# or - generator expression + have to account for when nothing is found (default val = None)

# stops when you've found the first match (doesn't loop through whole list) = increased performance
# movie_del = next((movie for movie in movies if int(movie["id"]) == int(id)), None)

# if movie_del == []:
# if movie_del is None:
# result = {"message": "movie not found"}
# return jsonify(result), 404

# movies.remove(movie_del[0])
# movies.remove(movie_del)
# result = {"messsage": "movie successfully deleted", "data": movie_del[0]}
# result = {"messsage": "movie successfully deleted", "data": movie_del}
# return jsonify(result)

# or Ragav's way
# if movie_del:
#   movies.remove(movie_del)
#   return jsonify({"message": "Deleted Successfully"})
# else:
#   return jsonify("message": "movie not found"), 404
# Persmission to modify the lexical scope variable | reassigning is not allowed
# global movies
# Now you can change the address
# movies = [movie for movie in movies if movie["id"] != id]
# return jsonify({"message": "Deleted Successfully"})


# @app.put("/movies/<id>")
# def update_movie(id):
# update_data = request.json
# this references the specific memory location and therefore when you change it, it changes it inplace
# does not make a copy of memory to save memory and improve performance
# specific_movie = next(
# (movie for movie in movies if int(movie["id"]) == int(id)), None  # same memory
# )
# if specific_movie is None:
# result = {"message": "movie not foumd"}
# return jsonify(result), 404
# update all values in "specific_movie" with values from "update_data" dictionary
# it changes in place!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# specific_movie.update(update_data)
# print(specific_movie)
# print(movies)

# or
# movie_idx = next(
# (idx for idx, movie in enumerate(movies) if movie["id"] == id), None
# )
# print(movies[movie_idx])
# or movies[movie_idx].update(update_data)
# movies[movie_idx] = {**movies[movie_idx], **update_data}
# print(movies)

# result = {"messsage": "movie successfully updated", "data": specific_movie}
# return jsonify(result)
