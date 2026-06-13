from flask import Flask, render_template, request, session, redirect
import config
import db
from destinations import get_destinations, add_destination, get_destination, update_destination, remove_destination, search, get_destinations_by_user, get_user_stats
from users import register_user, login_user, logout_user, get_user

app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    destinations = get_destinations()
    return render_template("index.html", destinations=destinations)

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return "VIRHE: salasanat eivät ole samat"

    if register_user(username, password1):
        return redirect("/")
    else:
        return "VIRHE: tunnus on jo varattu"

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/login_form", methods=["POST"])
def login_form():
    username = request.form["username"]
    password = request.form["password"]
    
    if login_user(username, password):
        return redirect("/")
    else:
        return "VIRHE: väärä tunnus tai salasana"

@app.route("/logout")
def logout():
    logout_user()
    return redirect("/")

@app.route("/destinations", methods=["GET"])
def destinations():
    destinations = get_destinations()
    return render_template("destinations.html", destinations=destinations, session=session)

@app.route("/new_destination", methods=["POST"])
def new_destination():
    if "user_id" not in session:
        return redirect("/login")

    name = request.form["name"]
    description = request.form["description"]
    user_id = session["user_id"]

    add_destination(name, description, user_id)
    destination_id = db.last_insert_id()
    return redirect("/destinations/" + str(destination_id))

@app.route("/destinations/<int:destination_id>")
def show_destination(destination_id):
    destination = get_destination(destination_id)
    return render_template("destination.html", destination=destination)

@app.route("/edit/<int:destination_id>", methods=["GET", "POST"])
def edit_destination(destination_id):
    destination = get_destination(destination_id)

    if request.method == "GET":
        return render_template("edit.html", destination=destination)

    if request.method == "POST":
        description = request.form["description"]
        update_destination(destination["destination_id"], description)
        return redirect("/destinations/" + str(destination["destination_id"]))

@app.route("/remove/<int:destination_id>", methods=["GET", "POST"])
def remove_trip_destination(destination_id):
    destination = get_destination(destination_id)

    if request.method == "GET":
        return render_template("remove.html", destination=destination)

    if request.method == "POST":
        if "continue" in request.form:
            remove_destination(destination["destination_id"])
        return redirect("/")

@app.route("/search")
def search_results():
    query = request.args.get("query")
    results = search(query) if query else []
    return render_template("search.html", query=query, results=results)

@app.route("/users/<int:user_id>")
def user_profile(user_id):
    user = get_user(user_id)
    if not user:
        return "Käyttäjää ei löytynyt", 404
    
    user_destinations = get_destinations_by_user(user_id)
    stats = get_user_stats(user_id)

    return render_template("user.html", user=user, destinations=user_destinations, stats=stats)
