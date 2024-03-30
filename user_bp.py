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
