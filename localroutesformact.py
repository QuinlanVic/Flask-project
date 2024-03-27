# ACTIONS FROM FORMS OLD (LOCALDATA)

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
