from flask import Blueprint, render_template
from flask_login import login_required

users = [
    {
        "id": "1",
        "name": "Dhara",
        "pic": "https://play-lh.googleusercontent.com/LeX880ebGwSM8Ai_zukSE83vLsyUEUePcPVsMJr2p8H3TUYwNg-2J_dVMdaVhfv1cHg",
        "pro": True,
    },
    {
        "id": "2",
        "name": "Gwen",
        "pic": "https://preview.redd.it/tt7kh1z7hpf91.png?auto=webp&s=28df0a3a48f989b5337a1d54ba9431065299197c",
        "pro": False,
    },
    {
        "id": "3",
        "name": "Shego",
        "pic": "https://w0.peakpx.com/wallpaper/828/185/HD-wallpaper-shego-kim.jpg",
        "pro": True,
    },
]

about_bp = Blueprint("about", __name__)


# /about page
@about_bp.route("/")
@login_required
def about_page():
    return render_template("about.html", users=users)


# specific user version of file
@about_bp.route("/<id>")
@login_required
def user_page(id):
    specific_user = [user for user in users if user["id"] == id]
    return render_template("about.html", users=specific_user)

    # <!-- {% extends 'base.html' %} {% block body %} -->
    #  {% endblock %}
