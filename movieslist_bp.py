from flask import Blueprint, render_template

from app import Movie, db


# Task - /movies/add -> Add movie form (5 fields = name, poster, rating, summary, trailer) -> Submit -> /movies-list
@movieslist_bp.route("/movieslist/add")
def add_movie_page():
    return render_template("addmovie.html")


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


@app.route("/movieslist/delete", methods=["POST"])
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
