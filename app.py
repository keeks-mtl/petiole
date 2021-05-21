import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from math import ceil
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


# check if username matches current user
def is_user(username):
    if "user" in session.keys():
        if session["user"] == username:
            return True

    return False


# Plants Page (all)
@app.route("/")
@app.route("/plants")
def plants():
    """
    Gets all plants from database.
    Divides the number of plants in database by number of plants on page.
    Renders plants page by plants and divides them into other pages.
    """
    plants_collection = mongo.db.plants
    page = int(request.args.get('page') or 1)
    # number of plants per page
    num = 12
    # finds how many pages there will be
    count = ceil(float(plants_collection.count_documents({}) / num))
    plants = list(plants_collection.find({}).sort("plant_like", -1).skip(
        (page - 1) * num).limit(num))
    return render_template(
        "plants.html", plants=plants,
        page=page, count=count, search=False)


# Register
@app.route("/register", methods=["GET", "POST"])
def register():
    """
    Checks if username already exists.
    Compiles inputs into a dictionary.
    Adds dictionary of inputs into the database.
    Adds user to session cookies
    """
    if request.method == "POST":
        # check if username already exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))

        # compile inputs into dictionary
        register = {
            "first_name": request.form.get("first_name").lower(),
            "last_name": request.form.get("last_name").lower(),
            "email": request.form.get("email"),
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password")),
            "liked_plant": []
        }
        # adds information from form into users database
        mongo.db.users.insert_one(register)

        # put the user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        flash("Registration Successful!")
        return redirect(url_for("profile", username=session["user"]))

    return render_template("register.html")


# Log In
@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Checks if username exists in database.
    Checks if user's username & password are correct.
    """
    if request.method == "POST":
        # check if username exists in database
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            # ensure hashed password matches user input
            if check_password_hash(
              existing_user["password"], request.form.get("password")):
                session["user"] = request.form.get("username").lower()
                return redirect(url_for(
                  "profile", username=session["user"]))

            else:
                # invalid password match
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))

        else:
            # username doesn't exist
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))

    return render_template("login.html")


# Profile Page
@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    """
    Checks if user is logged in.
    If user is logged in then shows them their profile page
    """

    # checks if session user is profile page's username
    if not is_user(username.lower()):
        return redirect(url_for("login"))

    # connects the user to their plants and renders page
    if session["user"]:
        plants = list(mongo.db.plants.find({"created_by": username}))
        return render_template(
            "profile.html", username=username, plants=plants)


# Sort Plants
@app.route("/sort", methods=["GET", "POST"])
def sort():
    """
    Get's information from sort form.
    Sort's plants on page by inputs
    """
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    if request.method == "POST":
        # get input from form
        sorted_by = request.form.get('sorted_by')
        if sorted_by != '':
            # sort plants by input option
            plants = list(mongo.db.plants.find({"created_by": username}).sort(sorted_by, 1))
            return render_template(
                "profile.html", plants=plants, username=username)

    # when sort option not chosen plants ordered by entry
    plants = list(mongo.db.plants.find({"created_by": username}))
    return render_template("profile.html", username=username, plants=plants)


# Log Out
@app.route("/logout")
def logout():
    # remove user from session cookies
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))


# Add Plant
@app.route("/add_plant", methods=["GET", "POST"])
def add_plant():
    """
    Checks if user is logged in, if not redirects to plants page.
    Converts data from form into dictionary and inserts that data
    into the database.
    """

    if request.method == "POST":
        # compiles inputs into dictionary
        toxic = "Yes" if request.form.get("toxic") else "No"
        humidity = "Yes, please" if request.form.get("humidity") else "No"
        suitable_for = request.form.getlist("suitable_for")
        plant = {
            "plant_latin_name": request.form.get("plant_latin_name"),
            "plant_common_name": request.form.get("plant_common_name"),
            "plant_image": request.form.get("plant_image"),
            "lighting": request.form.get("lighting"),
            "watering": request.form.get("watering"),
            "grow_speed": request.form.get("grow_speed"),
            "care": request.form.get("care"),
            "suitable_for": suitable_for,
            "toxic": toxic,
            "humidity": humidity,
            "created_by": session["user"],
            "plant_like": 0
        }
        # adds new plant into database
        mongo.db.plants.insert_one(plant)
        flash("Plant Successfully Added!")
        return redirect(url_for("profile", username=session["user"]))

    # checks if user is logged in
    if "user" in session:
        user = session["user"].lower()

        if user == session["user"].lower():
            return render_template("add_plant.html")

    # pevents users who are not logged in from accessing
    else:
        return redirect(url_for("plants"))


# Edit Plant
@app.route("/edit_plant/<plant_id>", methods=["GET", "POST"])
def edit_plant(plant_id):
    """
    Gathers information from database about plant from plant id.
    Checks if user created post, if not, redirect to login.
    Compiles all inputs into a dictionary to send to database
    Updates database
    """
    plant = mongo.db.plants.find_one({"_id": ObjectId(plant_id)})

    # checks if user is the user who created post
    if not is_user(plant["created_by"]):
        return redirect(url_for("login"))

    if request.method == "POST":
        # compiles inputs into dictionary
        toxic = "Yes" if request.form.get("toxic") else "No"
        humidity = "Yes, please" if request.form.get("humidity") else "No"
        submit = {
            "plant_latin_name": request.form.get("plant_latin_name"),
            "plant_common_name": request.form.get("plant_common_name"),
            "plant_image": request.form.get("plant_image"),
            "lighting": request.form.get("lighting"),
            "watering": request.form.get("watering"),
            "grow_speed": request.form.get("grow_speed"),
            "care": request.form.get("care"),
            "suitable_for": request.form.getlist("suitable_for"),
            "toxic": toxic,
            "humidity": humidity,
            "created_by": session["user"],
            "plant_like": plant["plant_like"]
        }
        # updates database with new inputs
        mongo.db.plants.update({"_id": ObjectId(plant_id)}, submit)
        flash("Plant Successfully Updated!")
        return redirect(url_for("profile", username=session["user"]))

    plant = mongo.db.plants.find_one({"_id": ObjectId(plant_id)})
    return render_template("edit_plant.html", plant=plant)


# Delete Plant
@app.route('/delete_plant/<plant_id>')
def delete_plant(plant_id):
    """
    Only allows users logged in to access.
    Checks if user logged in is user who created the plant card.
    """
    if "user" in session:
        user = session["user"].lower()

        if user == session["user"].lower():
            mongo.db.plants.remove({"_id": ObjectId(plant_id)})
            flash("Plant Successfully Deleted")
            return redirect(url_for("plants"))

    # pevents users who are not logged in from accessing
    else:
        return redirect(url_for("plants"))


# Plant Page of Specific Plant
@app.route("/plant_page/<plant_id>", methods=["GET", "POST"])
def plant_page(plant_id):
    """
    Displays information on plant to all users.
    Checks if user logged in has liked the plant.
    """
    # page initially rendered with grey heart
    plant = mongo.db.plants.find_one({"_id": ObjectId(plant_id)})
    is_liked = False
    # checks if the user is logged in
    if "user" in session:
        user = session["user"].lower()
        user_info = mongo.db.users.find_one({"username": user})
        # checks if plant_id is in user's liked_plant array
        if plant_id in user_info["liked_plant"]:
            # changes heart to red
            is_liked = True
    return render_template("plant_page.html", is_liked=is_liked, plant=plant)


# Like Plants
@app.route("/liked/<plant_id>", methods=["GET", "POST"])
def like_plant(plant_id):
    """
    Allows users the ability to like plants.
    Checks if user is logged in.
    When a plant is liked the plant's id is added to
    liked_plant array for user and the plant_like array
    is incremented.
    """
    plant = mongo.db.plants.find_one({"_id": ObjectId(plant_id)})
    # gets the user's session name and finds them in the database
    user = session["user"].lower()
    user_info = mongo.db.users.find_one(
        {"username": user})

    # looks for the plant_id in user's liked_plant array in database
    if plant_id not in user_info["liked_plant"]:
        # increments plant_like on the plants database entry
        mongo.db.plants.update({
            "_id": ObjectId(plant_id)},
            {"$inc": {"plant_like": +1}})
        # adds plant_id to liked_plant in user's database info
        mongo.db.users.update({
            "username": user},
            {"$push": {"liked_plant": plant_id}})
    # renders template with red heart
    return render_template(
        "plant_page.html", plant=plant,
        is_liked=True)


# Search Page
@app.route("/search", methods=["GET", "POST"])
def search():
    """
    Gives users the ability to search through all plants by filtering
    results by certain options.
    Options are :
        Plant name = Both common and latin names
        Lighting options
        Care options
        Whether plant is toxic
    Shows results with pagination.
    """
    if request.method == "POST":
        # link variables to form
        plant_name = request.form.get('plant_name')
        lighting = request.form.get('lighting')
        care = request.form.get('care')
        toxic = request.form.get('toxic')
        filter = {}
        categories = []
        # add variables to array
        if plant_name != '':
            categories.append(plant_name)
        if lighting != '':
            categories.append(lighting)
        if care != '':
            categories.append(care)
        if toxic != '':
            categories.append(toxic)
        # create filter of variables in search
        if categories is not None:
            filter = {'$text': {'$search': ', '.join(categories)}}
        # get filtered list of plants that were searched for
        plants = list(mongo.db.plants.find(filter))
        return render_template("search.html", plants=plants)

    # paginated plants when users initially visit search page
    plants_collection = mongo.db.plants
    page = int(request.args.get('page') or 1)
    num = 12
    count = ceil(float(plants_collection.count_documents({}) / num))
    plants = list(plants_collection.find({}).sort(
        "plant_latin_name", 1).skip((page - 1) * num).limit(num))
    return render_template(
        "search.html", plants=plants,
        page=page, count=count, search=False)


# 404 Handler
@app.errorhandler(404)
def page_not_found(error):
    """
    handles 404 errors
    """
    return render_template('404.html', title='404'), 404


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
