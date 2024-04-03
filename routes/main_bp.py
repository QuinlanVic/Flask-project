# blueprint for miscallaneous routes/pages
from flask import Blueprint, render_template


main_bp = Blueprint("main", __name__)


# home page
@main_bp.route("/")  # HOF (Higher Order Function)
def hello_world():
    return "<h1>Super, Cool 😁</h1>"


name = "Caleb"
hobbies = ["Gaming", "Reading", "Soccer", "Ballet", "Gyming"]


# /profile page
@main_bp.route("/profile")
def profile_page():
    return render_template("profile.html", name=name, hobbies=hobbies)


@main_bp.route("/sample")
def sample_page():
    return render_template("sample.html")
