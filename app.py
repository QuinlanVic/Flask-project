from flask import Flask

app = Flask(__name__)


# home page
@app.route("/")  # HOF
def hello_world():
    return "<h1>Super, Cool 😁</h1>"


# /about page
@app.route("/about")
def about():
    return "<h1>About</h1>"


# app.run(debug=True)
