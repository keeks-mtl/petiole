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


@app.route("/")
@app.route("/plants")
def plants():
    plants_collection = mongo.db.plants
    page = int(request.args.get('page') or 1)
    num = 12
    count = ceil(float(plants_collection.count_documents({}) / num))
    plants = list(plants_collection.find({}).skip((page - 1) * num).limit(num))
    return render_template(
        "plants.html", plants=plants,
        page=page, count=count, search=False)


@app.route("/sort", methods=["GET", "POST"])
def sort():
    if request.method == "POST":
        sorted_by = request.form.get('sorted_by')
        if sorted_by != '':
            username = mongo.db.users.find_one(
                {"username": session["user"]})["username"]
            plants = mongo.db.plants.find().sort(sorted_by, 1)
            return render_template(
                "profile.html", plants=plants, username=username)

    plants = mongo.db.plants.find()
    return render_template("profile.html", plants=plants)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # check if username already exists in db
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already exists")
            return redirect(url_for("register"))

        register = {
            "first_name": request.form.get("first_name").lower(),
            "last_name": request.form.get("last_name").lower(),
            "email": request.form.get("email"),
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password")),
            "liked_plant": []
        }
        mongo.db.users.insert_one(register)

        # put the user into 'session' cookie
        session["user"] = request.form.get("username").lower()
        flash("Registration Successful!")
        return redirect(url_for("profile", username=session["user"]))
    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # check if username exists in db
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


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    # grab the session user's username from db
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]

    if session["user"]:
        plants = list(mongo.db.plants.find().sort("plant_latin_name", 1))
        return render_template(
            "profile.html", username=username, plants=plants)

    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    # remove user from session cookies
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))


@app.route("/add_plant", methods=["GET", "POST"])
def add_plant():
    """
    Checks if user is logged in, if not redirects to ... page.
    Converts data from form into dict and inserts that data
    into the database.
    """

    if request.method == "POST":
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
        mongo.db.plants.insert_one(plant)
        flash("Plant Successfully Added!")
        return redirect(url_for("profile", username=session["user"]))

    # checks if user is logged in
    if "user" in session:
        user = session["user"].lower()

        if user == session["user"].lower():
            return render_template("add_plant.html")

        # prevent other registered user access
    else:
        return redirect(url_for("plants"))


@app.route("/edit_plant/<plant_id>", methods=["GET", "POST"])
def edit_plant(plant_id):
    """
    Gathers information from database about plant from plant id.
    Checks if is created post, if not, redirect to login.
    Compiles all inputs into a dictionary to send to database
    Updates database
    """
    plant = mongo.db.plants.find_one({"_id": ObjectId(plant_id)})

    if not is_user(plant["created_by"]):
        return redirect(url_for("login"))

    if request.method == "POST":
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
        mongo.db.plants.update({"_id": ObjectId(plant_id)}, submit)
        flash("Plant Successfully Updated!")
        return redirect(url_for("profile", username=session["user"]))

    plant = mongo.db.plants.find_one({"_id": ObjectId(plant_id)})
    return render_template("edit_plant.html", plant=plant)


@app.route('/delete_plant/<plant_id>')
def delete_plant(plant_id):
    mongo.db.plants.remove({"_id": ObjectId(plant_id)})
    flash("Plant Successfully Deleted")
    return redirect(url_for("plants"))


@app.route("/plant_page/<plant_id>", methods=["GET", "POST"])
def plant_page(plant_id):
    """
    Displays information on plant to all users.
    Checks if user logged in liked the plant.
    """
    plant = mongo.db.plants.find_one({"_id": ObjectId(plant_id)})
    is_liked = False
    if "user" in session:
        user = session["user"].lower()
        user_info = mongo.db.users.find_one({"username": user})
        if plant_id in user_info["liked_plant"]:
            is_liked = True
    return render_template("plant_page.html", is_liked=is_liked, plant=plant)


@app.route("/liked/<plant_id>", methods=["GET", "POST"])
def like_plant(plant_id):
    plant = mongo.db.plants.find_one({"_id": ObjectId(plant_id)})
    user = session["user"].lower()
    user_info = mongo.db.users.find_one(
        {"username": user})
    if plant_id not in user_info["liked_plant"]:
        mongo.db.plants.update({
            "_id": ObjectId(plant_id)},
            {"$inc": {"plant_like": +1}})
        mongo.db.users.update({
            "username": user},
            {"$push": {"liked_plant": plant_id}})
    return render_template(
        "plant_page.html", plant=plant,
        is_liked=True)


@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        plant_name = request.form.get('plant_name')
        lighting = request.form.get('lighting')
        care = request.form.get('care')
        toxic = request.form.get('toxic')
        filter = {}
        categories = []
        if plant_name != '':
            categories.append(plant_name)
        if lighting != '':
            categories.append(lighting)
        if care != '':
            categories.append(care)
        if toxic != '':
            categories.append(toxic)
        if categories is not None:
            filter = {'$text': {'$search': ', '.join(categories)}}
        plants = list(mongo.db.plants.find(filter))
        return render_template("search.html", plants=plants)

    plants_collection = mongo.db.plants
    page = int(request.args.get('page') or 1)
    num = 12
    count = ceil(float(plants_collection.count_documents({}) / num))
    plants = list(plants_collection.find({}).sort(
        "plant_latin_name", 1).skip((page - 1) * num).limit(num))
    return render_template(
        "search.html", plants=plants,
        page=page, count=count, search=False)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', title = '404'), 404


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
