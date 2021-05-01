import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
@app.route("/get_plants")
def get_plants():
    plants = mongo.db.plants.find()
    return render_template("plants.html", plants=plants)


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
            "first_name" : request.form.get("first_name").lower(),
            "last_name" : request.form.get("last_name").lower(),
            "email" : request.form.get("email"),
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(request.form.get("password"))
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
                    flash("Welcome, {}".format(
                        request.form.get("username")))
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
        return render_template("profile.html", username=username, plants=plants)

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
    loggedIn = True if 'user' in session else False

    if not loggedIn:
        return redirect(url_for("login"))

    if request.method =="POST":
        toxic = "Yes" if request.form.get("toxic") else "No"
        humidity = "Yes, please" if request.form.get("humidity") else "No"
        plant = {
            "plant_latin_name" : request.form.get("plant_latin_name"),
            "plant_common_name" : request.form.get("plant_common_name"),
            "plant_image" : request.form.get("plant_image"),
            "lighting" : request.form.get("lighting"),
            "watering" : request.form.get("watering"),
            "grow_speed" : request.form.get("grow_speed"),
            "care" : request.form.get("care"),
            "suitable_for" : request.form.get("suitable_for"),
            "toxic" : toxic,
            "humidity" : humidity,
            "created_by": session["user"]
        }
        mongo.db.plants.insert_one(plant)
        flash("Plant Successfully Added!")
        return redirect(url_for("profile", username=session["user"]))

    return render_template("add_plant.html")


@app.route("/edit_plant/<plant_id>", methods=["GET", "POST"])
def edit_plant(plant_id):
    if request.method =="POST":
        toxic = "Yes" if request.form.get("toxic") else "No"
        humidity = "Yes, please" if request.form.get("humidity") else "No"
        submit = {
            "plant_latin_name" : request.form.get("plant_latin_name"),
            "plant_common_name" : request.form.get("plant_common_name"),
            "plant_image" : request.form.get("plant_image"),
            "lighting" : request.form.get("lighting"),
            "watering" : request.form.get("watering"),
            "toxic" : toxic,
            "humidity" : humidity,
            "grow_speed" : request.form.get("grow_speed"),
            "created_by": session["user"]
        }
        mongo.db.plants.update({"_id": ObjectId(plant_id)}, submit)
        flash("Plant Successfully Updated!")

    plant = mongo.db.plants.find_one({"_id": ObjectId(plant_id)})
    return render_template("edit_plant.html", plant=plant)


@app.route('/delete_plant/<plant_id>')
def delete_plant(plant_id):
    mongo.db.plants.remove({"_id": ObjectId(plant_id)})
    flash("Plant Successfully Deleted")
    return redirect(url_for("get_plants"))


@app.route("/plant_page/<plant_id>", methods=["GET", "POST"])
def plant_page(plant_id):
    plant = mongo.db.plants.find_one({"_id": ObjectId(plant_id)})
    return render_template("plant_page.html", plant=plant)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
