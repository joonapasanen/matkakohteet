import sqlite3
from flask import Flask
from flask import render_template, request, session, redirect
from werkzeug.security import generate_password_hash, check_password_hash
import config
import db
from destinations import get_destinations, add_destination, get_destination, update_destination, remove_destination, search

app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    query = request.args.get("query", "")
    destinations = get_destinations()
    return render_template("index.html", query=query, destinations=destinations)

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
    password_hash = generate_password_hash(password1)

    try:
        sql = "INSERT INTO Users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hash])
        session["username"] = username
        session["user_id"] = db.last_insert_id()
        return redirect("/destinations")
        
    except sqlite3.IntegrityError:
        return "VIRHE: tunnus on jo varattu"
    
@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/login_form", methods=["POST"])
def login_form():
    username = request.form["username"]
    password = request.form["password"]
    
    sql = "SELECT password_hash, user_id FROM Users WHERE username = ?"
    password_hash = db.query(sql, [username])[0][0]
    user_id = db.query(sql, [username])[0][1]

    if check_password_hash(password_hash, password):
        session["username"] = username
        session["user_id"] = user_id

        return redirect("/destinations")
    else:
        return "VIRHE: väärä tunnus tai salasana"

@app.route("/logout")
def logout():
    del session["username"]
    redirect("/")

@app.route("/destinations", methods=["GET"])
def destinations():
    destinations = get_destinations()
    return render_template("destinations.html", destinations=destinations, session=session)

@app.route("/new_destination", methods=["POST"])
def new_thread():
    name = request.form["name"]
    description = request.form["description"]
    user_id = session["user_id"]

    thread_id = add_destination(name, description, user_id)
    return redirect("/destinations/" + str(thread_id))

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
        return redirect("/destinations")
    
@app.route("/search")
def search_results():
    query = request.args.get("query")
    results = search(query) if query else []
    return render_template("search.html", query=query, results=results)
