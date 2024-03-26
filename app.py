from flask import Flask, jsonify, request, render_template

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text

import os
from dotenv import load_dotenv
from pprint import pprint
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
    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(50))
    poster = db.Column(db.String(50))
    rating = db.Column(db.Float(50))
    summary = db.Column(db.String(50))
    trailer = db.Column(db.String(50))

    # JSON - Keys (can change names sent to front-end)
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "poster": self.poster,
            "rating": self.rating,
            "summary": self.summary,
            "trailer": self.trailer,
        }


# new get request getting data from azure
@app.get("/movies")
def get_movies():
    movie_list = Movie.query.all()  # SELECT * FROM movies | movie_list iterator
    data = [movie.to_dict() for movie in movie_list]  # convert to a list of dict
    # print(data)
    # print(type(jsonify(data)))
    # return jsonify(data)
    return data


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


# Task 1
# .all() - .get()
# <variable_name> -> becomes the keyword argument to "get_specific_movie"
@app.get("/movies/<id>")
def get_specific_movie(id):
    # print(type(id))  # string
    # movie_list = Movie.query.all()  # SELECT * FROM movies | movie_list iterator
    # data = [movie.to_dict() for movie in movie_list]  # convert to a list of dict
    # or - generator expression + have to account for when nothing is found (default val = None)
    # specific_movie = next((movie for movie in data if movie["id"] == id), None)
    # print(type(specific_movie))

    # get specific movie
    specific_movie2 = Movie.query.get(id)

    # if specific_movie == []:
    if specific_movie2 is None:
        result = {"message": "movie not found"}
        return jsonify(result), 404

    # convert to a dictionary
    data = specific_movie2.to_dict()
    result = {"message": "movie successfully found", "data": data}
    return jsonify(result)


movies = [
    {
        "id": "99",
        "name": "Vikram",
        "poster": "https://m.media-amazon.com/images/M/MV5BMmJhYTYxMGEtNjQ5NS00MWZiLWEwN2ItYjJmMWE2YTU1YWYxXkEyXkFqcGdeQXVyMTEzNzg0Mjkx._V1_.jpg",
        "rating": 8.4,
        "summary": "Members of a black ops team must track and eliminate a gang of masked murderers.",
        "trailer": "https://www.youtube.com/embed/OKBMCL-frPU",
    },
    {
        "id": "100",
        "name": "RRR",
        "poster": "https://englishtribuneimages.blob.core.windows.net/gallary-content/2021/6/Desk/2021_6$largeimg_977224513.JPG",
        "rating": 8.8,
        "summary": "RRR is an upcoming Indian Telugu-language period action drama film directed by S. S. Rajamouli, and produced by D. V. V. Danayya of DVV Entertainments.",
        "trailer": "https://www.youtube.com/embed/f_vbAtFSEc0",
    },
    {
        "id": "101",
        "name": "Iron man 2",
        "poster": "https://m.media-amazon.com/images/M/MV5BMTM0MDgwNjMyMl5BMl5BanBnXkFtZTcwNTg3NzAzMw@@._V1_FMjpg_UX1000_.jpg",
        "rating": 7,
        "summary": "With the world now aware that he is Iron Man, billionaire inventor Tony Stark (Robert Downey Jr.) faces pressure from all sides to share his technology with the military. He is reluctant to divulge the secrets of his armored suit, fearing the information will fall into the wrong hands. With Pepper Potts (Gwyneth Paltrow) and Rhodes (Don Cheadle) by his side, Tony must forge new alliances and confront a powerful new enemy.",
        "trailer": "https://www.youtube.com/embed/wKtcmiifycU",
    },
    {
        "id": "102",
        "name": "No Country for Old Men",
        "poster": "https://upload.wikimedia.org/wikipedia/en/8/8b/No_Country_for_Old_Men_poster.jpg",
        "rating": 8.1,
        "summary": "A hunter's life takes a drastic turn when he discovers two million dollars while strolling through the aftermath of a drug deal. He is then pursued by a psychopathic killer who wants the money.",
        "trailer": "https://www.youtube.com/embed/38A__WT3-o0",
    },
    {
        "id": "103",
        "name": "Jai Bhim",
        "poster": "https://m.media-amazon.com/images/M/MV5BY2Y5ZWMwZDgtZDQxYy00Mjk0LThhY2YtMmU1MTRmMjVhMjRiXkEyXkFqcGdeQXVyMTI1NDEyNTM5._V1_FMjpg_UX1000_.jpg",
        "summary": "A tribal woman and a righteous lawyer battle in court to unravel the mystery around the disappearance of her husband, who was picked up the police on a false case",
        "rating": 8.8,
        "trailer": "https://www.youtube.com/embed/nnXpbTFrqXA",
    },
    {
        "id": "104",
        "name": "The Avengers",
        "rating": 8,
        "summary": "Marvel's The Avengers (classified under the name Marvel Avengers\n Assemble in the United Kingdom and Ireland), or simply The Avengers, is\n a 2012 American superhero film based on the Marvel Comics superhero team\n of the same name.",
        "poster": "https://m.media-amazon.com/images/M/MV5BNDYxNjQyMjAtNTdiOS00NGYwLWFmNTAtNThmYjU5ZGI2YTI1XkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_.jpg",
        "trailer": "https://www.youtube.com/embed/eOrNdBpGMv8",
    },
    {
        "id": "105",
        "name": "Interstellar",
        "poster": "https://m.media-amazon.com/images/I/A1JVqNMI7UL._SL1500_.jpg",
        "rating": 8.6,
        "summary": "When Earth becomes uninhabitable in the future, a farmer and ex-NASA\n pilot, Joseph Cooper, is tasked to pilot a spacecraft, along with a team\n of researchers, to find a new planet for humans.",
        "trailer": "https://www.youtube.com/embed/zSWdZVtXT7E",
    },
    {
        "id": "106",
        "name": "Baahubali",
        "poster": "https://flxt.tmsimg.com/assets/p11546593_p_v10_af.jpg",
        "rating": 8,
        "summary": "In the kingdom of Mahishmati, Shivudu falls in love with a young warrior woman. While trying to woo her, he learns about the conflict-ridden past of his family and his true legacy.",
        "trailer": "https://www.youtube.com/embed/sOEg_YZQsTI",
    },
    {
        "id": "107",
        "name": "Ratatouille",
        "poster": "https://resizing.flixster.com/gL_JpWcD7sNHNYSwI1ff069Yyug=/ems.ZW1zLXByZC1hc3NldHMvbW92aWVzLzc4ZmJhZjZiLTEzNWMtNDIwOC1hYzU1LTgwZjE3ZjQzNTdiNy5qcGc=",
        "rating": 8,
        "summary": "Remy, a rat, aspires to become a renowned French chef. However, he fails to realise that people despise rodents and will never enjoy a meal cooked by him.",
        "trailer": "https://www.youtube.com/embed/NgsQ8mVkN8w",
    },
    {
        "name": "PS2",
        "poster": "https://m.media-amazon.com/images/M/MV5BYjFjMTQzY2EtZjQ5MC00NGUyLWJiYWMtZDI3MTQ1MGU4OGY2XkEyXkFqcGdeQXVyNDExMjcyMzA@._V1_.jpg",
        "summary": "Ponniyin Selvan: I is an upcoming Indian Tamil-language epic period action film directed by Mani Ratnam, who co-wrote it with Elango Kumaravel and B. Jeyamohan",
        "rating": 8,
        "trailer": "https://www.youtube.com/embed/KsH2LA8pCjo",
        "id": "108",
    },
    {
        "name": "Thor: Ragnarok",
        "poster": "https://m.media-amazon.com/images/M/MV5BMjMyNDkzMzI1OF5BMl5BanBnXkFtZTgwODcxODg5MjI@._V1_.jpg",
        "summary": "When Earth becomes uninhabitable in the future, a farmer and ex-NASA\\n pilot, Joseph Cooper, is tasked to pilot a spacecraft, along with a team\\n of researchers, to find a new planet for humans.",
        "rating": 8.8,
        "trailer": "https://youtu.be/NgsQ8mVkN8w",
        "id": "109",
    },
]


# home page
@app.route("/")  # HOF (Higher Order Function)
def hello_world():
    return "<h1>Super, Cool 😁</h1>"


users = [
    {
        "name": "Dhara",
        "pic": "https://play-lh.googleusercontent.com/LeX880ebGwSM8Ai_zukSE83vLsyUEUePcPVsMJr2p8H3TUYwNg-2J_dVMdaVhfv1cHg",
        "pro": True,
    },
    {
        "name": "Gwen",
        "pic": "https://preview.redd.it/tt7kh1z7hpf91.png?auto=webp&s=28df0a3a48f989b5337a1d54ba9431065299197c",
        "pro": False,
    },
    {
        "name": "Shego",
        "pic": "https://w0.peakpx.com/wallpaper/828/185/HD-wallpaper-shego-kim.jpg",
        "pro": True,
    },
]


# /about page
@app.route("/about")
def about_page():
    return render_template("about.html", users=users)


name = "Caleb"
hobbies = ["Gaming", "Reading", "Soccer", "Ballet", "Gyming"]


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


# Task - /movies/add -> Add movie form (5 fields = name, poster, rating, summary, trailer) -> Submit -> /movies-list
@app.route("/movies/add")
def add_movie_page():
    return render_template("addmovie.html")


@app.route("/movieslist", methods=["POST"])
def new_movie_list():
    movie_name = request.form.get("name")
    movie_poster = request.form.get("poster")
    movie_rating = request.form.get("rating")
    movie_summary = request.form.get("summary")
    movie_trailer = request.form.get("trailer")
    newmovie = {
        "name": movie_name,
        "poster": movie_poster,
        "rating": float(movie_rating),
        "summary": movie_summary,
        "trailer": movie_trailer,
    }
    movie_ids = [int(movie["id"]) for movie in movies]
    max_id = max(movie_ids)
    print(max_id)
    # or
    newmovie["id"] = str(max_id + 1)
    movies.append(newmovie)
    return render_template("movies-list.html", movies=movies)


# Spider-Man 2
# https://m.media-amazon.com/images/M/MV5BMzY2ODk4NmUtOTVmNi00ZTdkLTlmOWYtMmE2OWVhNTU2OTVkXkEyXkFqcGdeQXVyMTQxNzMzNDI@._V1_.jpg
# 7.5
# Peter Parker is beset with troubles in his failing personal life as he battles a former brilliant scientist named Otto Octavius.
# https://www.imdb.com/video/vi629801241/?playlistId=tt0316654&ref_=tt_pr_ov_vi


# GET -> movies page -> JSON
# @app.get("/movies")
# def get_movies():
# have to convert to JSON (using jsonify library from Flask)
# return jsonify(movies)


# POST -> request.json -> create movie + add to movies list -> JSON
# 1 more than the max id
@app.post("/movies")
def create_movie():
    # get new movie JSON data from body in request
    new_movie = request.json
    movie_ids = [int(movie["id"]) for movie in movies]
    # print(movie_ids)
    max_id = max(movie_ids)
    print(max_id)
    # dictionary
    # print(type(new_movie))
    # new_movie = {**new_movie, "id": str(max_id + 1)}

    # or
    new_movie["id"] = str(max_id + 1)
    # check if movie is correctly updated with new id
    print(new_movie)
    # add to movies list of dict
    movies.append(new_movie)
    # create message to return
    result = {"message": "added successfully", "data": new_movie}
    # added status code
    return jsonify(result), 201


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
@app.delete("/movies/<id>")
def delete_movie(id):
    # movie_del = [movie for movie in movies if int(movie["id"]) == int(id)]

    # or - generator expression + have to account for when nothing is found (default val = None)

    # stops when you've found the first match (doesn't loop through whole list) = increased performance
    movie_del = next((movie for movie in movies if int(movie["id"]) == int(id)), None)

    # if movie_del == []:
    if movie_del is None:
        result = {"message": "movie not found"}
        return jsonify(result), 404

    # movies.remove(movie_del[0])
    movies.remove(movie_del)
    # result = {"messsage": "movie successfully deleted", "data": movie_del[0]}
    result = {"messsage": "movie successfully deleted", "data": movie_del}
    return jsonify(result)

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


@app.put("/movies/<id>")
def update_movie(id):
    update_data = request.json
    # this references the specific memory location and therefore when you change it, it changes it inplace
    # does not make a copy of memory to save memory and improve performance
    specific_movie = next(
        (movie for movie in movies if int(movie["id"]) == int(id)), None  # same memory
    )
    if specific_movie is None:
        result = {"message": "movie not foumd"}
        return jsonify(result), 404
    # update all values in "specific_movie" with values from "update_data" dictionary
    # it changes in place!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    specific_movie.update(update_data)
    print(specific_movie)
    # print(movies)

    # or
    # movie_idx = next(
    # (idx for idx, movie in enumerate(movies) if movie["id"] == id), None
    # )
    # print(movies[movie_idx])
    # or movies[movie_idx].update(update_data)
    # movies[movie_idx] = {**movies[movie_idx], **update_data}
    # print(movies)

    result = {"messsage": "movie successfully updated", "data": specific_movie}
    return jsonify(result)
