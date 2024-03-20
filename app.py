from flask import Flask, jsonify, request

app = Flask(__name__)


# home page
@app.route("/")  # HOF
def hello_world():
    return "<h1>Super, Cool 😁</h1>"


# /about page
@app.route("/about")
def about():
    return "<h1>About</h1>"


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
        "poster": "https://terrigen-cdn-dev.marvel.com/content/prod/1x/avengersendgame_lob_crd_05.jpg",
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


# /movies -> JSON


# GET -> movies page -> JSON
@app.get("/movies")
def get_movies():
    # have to convert to JSON (using jsonify using library from Flask)
    return jsonify(movies)


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
@app.get("/movies/<id>")
def get_specific_movie(id):
    print(type(id))
    # specific_movie = [movie for movie in movies if int(movie["id"]) == int(id)]

    # or - generator expression + have to account for when nothing is found (default val = None)
    specific_movie = next(
        (movie for movie in movies if int(movie["id"]) == int(id)), None
    )
    # print(type(specific_movie))

    # if specific_movie == []:
    if specific_movie is None:
        result = {"message": "movie not found"}
        return jsonify(result), 404

    # result = {"message": "movie successfully found", "data": specific_movie[0]}
    result = {"message": "movie successfully found", "data": specific_movie}
    return jsonify(result)


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
    specific_movie = next(
        (movie for movie in movies if int(movie["id"]) == int(id)), None
    )
    if specific_movie is None:
        result = {"message": "movie not foumd"}
        return jsonify(result), 404
    # update all values in "specific_movie" with values from "update_data" dictionary
    # it changes in place
    specific_movie.update(update_data)
    print(specific_movie)
    # print(movies)

    result = {"messsage": "movie successfully updated", "data": specific_movie}
    return jsonify(result)
