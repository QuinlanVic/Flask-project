from flask import Blueprint, render_template, redirect, url_for, request, abort, flash

from flask_wtf import FlaskForm

from extensions import db

from models.user import User

from werkzeug.security import generate_password_hash, check_password_hash

# from django.utils.http import url_has_allowed_host_and_scheme

user_bp = Blueprint("user", __name__)


from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError

from flask_login import login_user, logout_user, login_required


# registration validation
class RegistrationForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=6)])
    password = PasswordField(
        "Password", validators=[InputRequired(), Length(min=8, max=12)]
    )
    submit = SubmitField("Sign Up")

    # use WTF to send user back to registration page if input is invalid
    # automatically runs when the "form.validate_on_submit()" function executes
    # class method (instance and data from user form via field)
    # validate = function name and then "_" then the field name
    def validate_username(self, field):
        # inform WTF that there is an error and display it
        print("Validate username was called (reg)", field.data)
        specific_user = User.query.filter_by(username=field.data).first()
        # print(specific_user)

        # if it does exist then user cannot sign up and send them back to register page
        if specific_user:
            # the message below is displayed in the "div" in the register form
            raise ValidationError("Username taken")


# login validation
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    submit = SubmitField("Login")

    # validate = function name and then "_" then the field name
    def validate_username(self, field):
        # inform WTF that there is an error and display it
        print("Validate username was called (log)", field.data)
        specific_user = User.query.filter_by(username=field.data).first()
        # print(specific_user)

        # if it does not exist then user cannot log in and we send them back to login page
        if not specific_user:
            # the message below is displayed in the "div" in the register form
            raise ValidationError("Username or password invalid")

    # Validate for login form
    def validate_password(self, field):
        # access username via self
        user = User.query.filter_by(username=self.username.data).first()
        if user:
            if not check_password_hash(user.password, field.data):
                raise ValidationError("Username or password is invalid")


# GET - Issue token
# POST - Verify token
# new route for login page
@user_bp.route("/login", methods=["GET", "POST"])  # HOF
def login_page():
    # GET & POST
    # create a new form object
    form = LoginForm()

    # only on POST (when user is registering)
    if form.validate_on_submit():
        # check if username is already in database
        specific_user = User.query.filter_by(username=form.username.data).first()
        # test if correct user
        print(specific_user)

        # if it does not exist then user cannot sign up and send them back to register page
        if not specific_user:
            # flash("Invalid username or password", "danger")
            return render_template("login.html", form=form)

        # otherwise user has logged in successfully
        # token is issued - cookies stored in the browser
        login_user(specific_user)
        flash("You have been successfully logged in " + f"{specific_user.username} :)")
        next = request.args.get("next")
        # url_has_allowed_host_and_scheme should check if the url is safe
        # for redirects, meaning it matches the request host.
        # if not url_has_allowed_host_and_scheme(next, request.host):
        #     return abort(400)

        # return f"<h1>Welcome back, {form.username.data}"
        return redirect(next or url_for("movieslist.movie_list_page"))

    # only on GET
    # then use it in register page
    return render_template("login.html", form=form)


# GET - Issue token
# POST - Verify token
# new route for register page
@user_bp.route("/register", methods=["GET", "POST"])  # HOF
def register_page():
    # GET & POST
    # create a new form object
    form = RegistrationForm()

    # only on POST (when user is registering)
    if form.validate_on_submit():
        # check if username is already in database
        # specific_user = User.query.get(form.username.data)
        # specific_user = db.session.query(User).filter(
        #     User.username == (form.username.data)
        # )
        # or
        specific_user = User.query.filter_by(username=form.username.data).first()
        print(specific_user)

        # if it does exist then user cannot sign up and send them back to register page
        if specific_user:
            return render_template("register.html", form=form)
        # otherwise create a new user entry
        # print(form.username.data, form.password.data)
        # add registered users to the database
        password_hash = generate_password_hash(form.password.data)
        print(form.password.data, password_hash)
        new_user = User(
            username=form.username.data,
            password=password_hash,
        )  # id should be auto-created
        try:
            db.session.add(new_user)
            db.session.commit()
            # print("Profile page", username, password)
            # otherwise user has logged in successfully
            login_user(new_user)
            flash("<h1>You have been successfully logged in</h1")
            next = request.args.get("next")
            # url_has_allowed_host_and_scheme should check if the url is safe
            # for redirects, meaning it matches the request host.
            # if not url_has_allowed_host_and_scheme(next, request.host):
            #     return abort(400)

            # return f"<h1>Welcome back, {form.username.data}"
            return redirect(next or url_for("movieslist.movie_list_page"))
            # return "<h1> Registration successful </h1>", 201
        # now send them to new profile page
        # return render_template("profile.html", new_user.to_dict())
        except Exception as e:
            db.session.rollback()  # undo the change (unless committed already)
            return f"<h1>An error occured: {str(e)}", 500

    # only on GET
    # then use it in register page
    return render_template("register.html", form=form)


@user_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("movieslist.movie_list_page"))


# *********** OLD USER CRUD OPERATIONS WITH DB ********************
# # log a user in
# @app.route("/user", methods=["POST"])  # HOF
# def dashboard_page():
#     # have to get values from form via keys
#     username = request.form.get("username")
#     password = request.form.get("password")
#     # check if username and password match
#     specific_user = User.query.get(username)
#     # if the username or password is incorrect they cannot log in
#     if not specific_user or specific_user.password != password:
#         return f"<h1>Username or password is incorrect, please try again :)</h1>"
#     # otherwise log the user in
#     print("Dashboard page", username, password)
#     return f"<h1>Hi {username}, welcome back to our Movies App 🙂</h1>"


# # get a user by id
# # specific movie page
# @app.route("/user/<id>")
# def profile_page(id):
#     specific_user = User.query.get(id)
#     if specific_user is None:
#         return "<h1>User not found</h1>"
#     return render_template("profile.html", movie=specific_user.to_dict())


# # sign a user up
# @app.route("/user/profile", methods=["POST"])  # HOF
# def profile_page2():
#     # have to get values from form via keys
#     username = request.form.get("username")
#     password = request.form.get("password")
#     # check if username is already in database
#     specific_user = User.query.get(username)
#     # if it does exist then user cannot sign up
#     if specific_user:
#         return f"<h1>User already exists, please input a different username :)</h1>"
#     # otherwise create a new user entry
#     new_user = User(username=username, password=password)  # id should be auto-created
#     try:
#         db.session.add(new_user)
#         db.session.commit()
#         print("Profile page", username, password)
#         # now send them to new profile page
#         # return f"<h1>Hi {username}, welcome to our Movies App 🙂</h1>"
#         return render_template("profile.html", new_user.to_dict())
#     except Exception as e:
#         db.session.rollback()  # undo the change (unless committed already)
#         return f"<h1>An error occured: {str(e)}", 500


# # Delete a user from FORM
# @app.route("/user/delete", methods=["POST"])
# def delete_user_by_id():
#     id = request.form.get("user_id")
#     user = User.query.get(id)

#     # if user is not found
#     if not user:
#         return "<h1>User not found</h1>", 404

#     # otherwise delete it
#     try:
#         db.session.delete(user)
#         db.session.commit()
#         return f"<h1>{user.username} successfully deleted"
#     except Exception as e:
#         return f"<h1>An error occured: {str(e)}</h1>", 500


# # update user form route
# # Task - /user/update -> Update user form (2 existing fields = username and password) -> Submit -> /users
# # Has to be post to pass the data for some reason?
# # take you to update form with data after manipulation
# @app.route("/user/update", methods=["POST"])
# def update_user_page():
#     user = request.form.get("user")
#     print(user)
#     print(type(user))
#     # funny error as JSON only supports single quotes LOLOLOLOLOL
#     user_json = user.replace("'", '"')
#     # convert into a dict
#     user_dict = json.loads(user_json)
#     print(type(user_dict))
#     return render_template("updateuser.html", movie=user_dict)


# # UPDATE USER FORM TO SQL DATABASE
# # has to be a different url or it will do the other "/update" above as
# # it also uses a POST method because it has to for passing data for some reason
# @app.route("/user/update/db", methods=["POST"])
# def update_user_list():
#     user_id = request.form.get("id")
#     update_data = {
#         "username": request.form.get("username"),
#         "password": request.form.get("password"),
#     }
#     specific_user = User.query.get(user_id)
#     if specific_user is None:
#         return "<h1>User not found</h1>"
#     try:
#         # update all values in "specific_user" with values from "update_data" dictionary
#         # loop body as you only want to work with specific keys we need to update
#         for key, value in update_data.items():
#             # if they put in random keys it will change it which is unsafe!!!!
#             # specific_user.key = update_data.get(key, specific_user.key)
#             # so now we check if the key is in the table and only work with it if it is
#             if hasattr(specific_user, key):
#                 # now update those values
#                 setattr(specific_user, key, value)
#         db.session.commit()
#         return f"{specific_user.username} successfully updated"
#     except Exception as e:
#         return f"<h1>An error occured: {str(e)}"
