from flask import Blueprint, jsonify, request
from flask_sqlalchemy import SQLAlchemy

from app import Movie, db

# THESE ARE FOR JSON REQUESTS BY FRONT-END DEVELOPERS

# or no import and this code
# class Movie(db.Model):
#     __tablename__ = "movies"
#     # automatically creates and assigned value
#     # increased performance if you do not do calculations to update id by max id on the python side
#     # if autoincremented on the SQL side it will not have a decrease in preformance as it will remember the last value and update easily
#     # increased security as it is more difficult for people to guess "id" values
#     # easier to merge two tables as their id primary keys will not be the same/consist of duplicates
#     id = db.Column(db.String(50), primary_key=True, default=lambda: str(uuid.uuid4()))
#     name = db.Column(db.String(50))
#     poster = db.Column(db.String(50))
#     rating = db.Column(db.Float(50))
#     summary = db.Column(db.String(50))
#     trailer = db.Column(db.String(50))

#     # JSON - Keys (can change names sent to front-end)
#     # dict is also easier to convert to JSON
#     def to_dict(self):
#         return {
#             "id": self.id,
#             "name": self.name,
#             "poster": self.poster,
#             "rating": self.rating,
#             "summary": self.summary,
#             "trailer": self.trailer,
#         }
# db = SQLAlchemy()

movies_bp = Blueprint("movies", __name__)


# ALL "MOVIES" URLS
# ONLY JSON REQUESTS TO DATABASE


# get all movies from azure request
@movies_bp.get("/")
def get_movies():
    movie_list = Movie.query.all()  # SELECT * FROM movies | movie_list iterator
    data = [movie.to_dict() for movie in movie_list]  # convert to a list of dict
    # print(data)
    # print(type(jsonify(data)))
    # return jsonify(data)
    return data


# Task 1
# .all() = .get()
# <variable_name> -> becomes the keyword argument to "get_specific_movie"
# Get a specific movie from azure request
@movies_bp.get("/<id>")
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


# POST -> request.json -> create movie + add to movies list -> JSON
# 1 more than the max id
# Create a new movie and add it to azure db request
@movies_bp.post("/")
def create_movie():
    # get new movie JSON data from body in request
    data = request.json
    # create a new movie with it, noo id as it is automatically created and asigned
    new_movie = Movie(
        name=data["name"],
        poster=data["poster"],
        rating=data["rating"],
        summary=data["summary"],
        trailer=data["trailer"],
    )
    # if keys of Model and keys of data sent from users side are the same then you can use unpacking
    # risk = if they provide an "id" value it is added (not automatically generated)
    # definitely a work-around
    # new_movie = Movie(**data)
    try:
        db.session.add(new_movie)
        db.session.commit()
        # check if movie is correctly updated
        print(new_movie)
        # create message to return
        result = {"message": "added successfully", "data": new_movie.to_dict()}
        # added status code
        return jsonify(result), 201
    except Exception as e:
        # roll back changes before changing the data (unless committed already)
        db.session.rollback()
        # server error
        result = {"error": str(e)}
        return jsonify(result), 500


# movie.name = update_data['name']
# db.session.commit()
# Update specific movie and add to azure db request
@movies_bp.put("/<id>")
def update_movie(id):
    update_data = request.json
    # this references the specific memory location and therefore when you change it, it changes it inplace
    # does not make a copy of memory to save memory and improve performance
    specific_movie = Movie.query.get(id)
    if specific_movie is None:
        result = {"message": "movie not foumd"}
        return jsonify(result), 404
    try:
        # update all values in "specific_movie" with values from "update_data" dictionary
        # use "data.get" so that it doesn't throw an error and we give the original value as the default value
        # if the key is not supplied to be changed
        # specific_movie.name = update_data.get("name", specific_movie.name)
        # specific_movie.poster = update_data.get("poster", specific_movie.poster)
        # specific_movie.rating = update_data.get("rating", specific_movie.rating)
        # specific_movie.summary = update_data.get("summary", specific_movie.summary)
        # specific_movie.trailer = update_data.get("trailer", specific_movie.trailer)
        # loop body as you only want to work with specific keys we need to update
        for key, value in update_data.items():
            # if they put in random keys it will change it which is unsafe!!!!
            # specific_movie.key = update_data.get(key, specific_movie.key)
            # so now we check if the key is in the table and only work with it if it is
            if hasattr(specific_movie, key):
                # now update those values
                setattr(specific_movie, key, value)
        db.session.commit()
        # print(specific_movie)
        # print(movies)
        result = {
            "messsage": "movie successfully updated",
            "data": specific_movie.to_dict(),
        }
        return jsonify(result)
    except Exception as e:
        result = {"error": str(e)}
        return jsonify(result), 500


# Task 4 | db.session.delete(movie)
# create delete API for movies
# Delete the specific movie from azure db request
@movies_bp.delete("/<id>")
def delete_movie(id):
    movie_del = Movie.query.get(id)
    if not movie_del:
        # if we did not find it
        result = {"message": "movie not found"}
        return jsonify(result), 404
    try:
        # delete from database (not permanently)
        db.session.delete(movie_del)
        db.session.commit()  # making the change permanent (any change i.e., delete or update)
        result = {"messsage": "movie successfully deleted", "data": movie_del.to_dict()}
        return jsonify(result)
    except Exception as e:
        # roll back changes before changing the data (unless committed already)
        db.session.rollback()
        # server error
        result = {"error": str(e)}
        return jsonify(result), 500


# # ***************** THESE ARE OLD JSON REQUESTS BY FRONT-END DEVELOPERS FOR USERS *******************


# # Get a specific user from azure request
# @app.get("/user/<id>")
# def get_specific_user(id):
#     # get specific user
#     specific_user = User.query.get(id)

#     if specific_user is None:
#         result = {"message": "user not found"}
#         return jsonify(result), 404

#     # convert to a dictionary
#     data = specific_user.to_dict()
#     result = {"message": "user successfully found", "data": data}
#     return jsonify(result)


# # Create a new user and add it to azure db request
# @app.post("/")
# def create_user():
#     # get new user JSON data from body in request
#     data = request.json
#     # create a new user with it, not id as it is automatically created and asigned
#     new_user = User(username=data["username"], password=data["password"])
#     # if keys of Model and keys of data sent from users side are the same then you can use unpacking
#     # risk = if they provide an "id" value it is added (not automatically generated)
#     # definitely a work-around
#     # new_user = User(**data)
#     try:
#         db.session.add(new_user)
#         db.session.commit()
#         # check if user is correctly updated
#         print(new_user)
#         # create message to return
#         result = {"message": "user added successfully", "data": new_user.to_dict()}
#         # added status code
#         return jsonify(result), 201
#     except Exception as e:
#         # roll back changes before changing the data (unless committed already)
#         db.session.rollback()
#         # server error
#         result = {"error": str(e)}
#         return jsonify(result), 500
