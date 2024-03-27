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
