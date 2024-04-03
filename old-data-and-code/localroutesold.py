# Get all movies route (local data old)
# @app.route("/dashboard2")
# def dashboard_page2():
#     return render_template("dashboard2.html", movies=movies)


# Task 2 - get movies from database
# Get all movies route (local data)
# @app.route("/movieslist")
# def movie_list_page():
#     return render_template("movies-list.html", movies=movies)


# Get specific movie route (local data)
# @app.route("/movieslist/<id>")
# def movie_page(id):
# movie = get_specific_movie(id)
# specific_movie = next((movie for movie in movies if movie["id"] == id), None)
# if specific_movie is None:
#     result = {"message": "movie not found"}
#     return "<h1>Movie not found</h1>"
# result = {"message": "movie successfully found", "data": specific_movie}
# return render_template("movie.html", movie=specific_movie)


# Task - /movies/update -> update movie form (5 fields = name, poster, rating, summary, trailer) -> Submit -> /movies-list
# @app.route("/movies/update")
# def add_movie_page():
#     return render_template("updatemovie.html")
