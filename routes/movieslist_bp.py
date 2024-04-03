from flask import Blueprint, render_template, request

from extensions import db

from models.movie import Movie

import json

movieslist_bp = Blueprint("movieslist", __name__)

# ********* ALL MOVIESLIST URLS ***********
# Defines View part of web application

# OLD LOGIN AND SIGNUP
# Go to login page
# @app.route("/login")  # HOF
# def login_page():
#     return render_template("login.html")


# Go to signup page
# @app.route("/signup")  # HOF
# def signup_page():
#     return render_template("signup.html")


# Task - /movieslist/add -> Add movie form (5 fields = name, poster, rating, summary, trailer) -> Submit -> /movies-list
@movieslist_bp.route("/add")
def add_movie_page():
    return render_template("addmovie.html")


# Task - /movieslist/update -> Update movie form (5 existing fields = name, poster, rating, summary, trailer) -> Submit -> /movies-list
# Has to be post to pass the data via body (get uses URL)
# take you to update form with data after manipulation
@movieslist_bp.route("/update", methods=["POST"])
def update_movie_page():
    movie = request.form.get("movie")
    print(movie)
    print(type(movie))
    # funny error as JSON only supports single quotes LOLOLOLOLOL
    movie_json = movie.replace("'", '"')
    # convert into a dict
    movie_dict = json.loads(movie_json)
    print(type(movie_dict))
    return render_template("updatemovie.html", movie=movie_dict)


# movies list
@movieslist_bp.route("/", methods=["GET", "POST"])
def movie_list_page():
    movie_list = Movie.query.all()  # SELECT * FROM movies | movie_list iterator
    # print(type(movie_list)) # list
    # print(type(movie_list[0])) # app.Movie
    data = [movie.to_dict() for movie in movie_list]  # convert to a list of dict
    return render_template("movies-list.html", movies=data)


# Task 3 - display the data for specific movie on page
# specific movie page
@movieslist_bp.route("/<id>")
def movie_page(id):
    specific_movie = Movie.query.get(id)

    if specific_movie is None:
        return "<h1>Movie not found</h1>"

    return render_template("movie.html", movie=specific_movie.to_dict())


# ***** FORM ACTION CRUD OPERATIONS *****


@movieslist_bp.route("/delete", methods=["POST"])
def delete_movie_by_id():
    id = request.form.get("movie_id")  # get name from form
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
@movieslist_bp.route("/add/db", methods=["POST"])
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


# Spider-Man 2
# https://m.media-amazon.com/images/M/MV5BMzY2ODk4NmUtOTVmNi00ZTdkLTlmOWYtMmE2OWVhNTU2OTVkXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_.jpg
# 7.5
# Peter Parker is beset with troubles in his failing personal life as he battles a former brilliant scientist named Otto Octavius.
# https://www.imdb.com/video/vi629801241/?playlistId=tt0316654&ref_=tt_pr_ov_vi


# UPDATE MOVIE FORM TO SQL DATABASE NOW NOT LOCAL
# has to be a different url or it will do the other "/update" above as
# it also uses a POST method because it has to for passing data via body (get uses URL)
@movieslist_bp.route("/update/db", methods=["POST"])
def update_movie_list():
    movie_id = request.form.get("id")
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
    specific_movie = Movie.query.get(movie_id)
    if specific_movie is None:
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
        return f"{specific_movie.name} successfully updated"
    except Exception as e:
        return f"<h1>An error occured: {str(e)}"
