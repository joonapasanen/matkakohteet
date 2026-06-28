from flask import Flask, render_template, request, session, redirect, flash
import config
from destinations import get_destinations, add_destination, get_destination, update_destination, remove_destination, search, get_destinations_by_user, get_user_stats, get_categories, get_destination_categories
from users import register_user, login_user, logout_user, get_user
from comments import add_comment, get_comments, get_comment, remove_comment

app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    destinations = get_destinations()
    categories = get_categories()
    return render_template("index.html", destinations=destinations, categories=categories)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html", filled={})

    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        flash("VIRHE: Salasanat eivät ole samat")
        return render_template("register.html", filled={"username": username})

    if register_user(username, password1):
        return redirect("/")
    else:
        flash("VIRHE: Tunnus on jo varattu")
        return render_template("register.html", filled={"username": username})

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html", filled={})

    username = request.form["username"]
    password = request.form["password"]
    if login_user(username, password):
        return redirect("/")
    else:
        flash("VIRHE: Väärä tunnus tai salasana")
        return render_template("login.html", filled={"username": username})

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
    
    csrf_token = request.form.get("csrf_token")
    if csrf_token != session.get("csrf_token"):
        flash("VIRHE: CSRF-virhe")
        return redirect("/")

    name = request.form["name"].strip()
    description = request.form["description"].strip()
    user_id = session["user_id"]

    if not name:
        flash("VIRHE: Ei syötettä")
        return redirect("/new_destination")
    if len(name) > 75 or len(description) > 5000:
        flash("VIRHE: Liian pitkä syöte")
        return redirect("/new_destination")

    categories = []
    
    for entry in request.form.getlist("categories"):
        if entry:
            parts = entry.split(":")
            categories.append((parts[0], parts[1]))
    
    destination_id = add_destination(name, description, user_id, categories)
    return redirect("/destinations/" + str(destination_id))

@app.route("/destinations/<int:destination_id>")
def show_destination(destination_id):
    destination = get_destination(destination_id)
    categories = get_destination_categories(destination_id)
    comments = get_comments(destination_id)
    return render_template("destination.html", destination=destination, categories=categories, comments=comments)

@app.route("/edit/<int:destination_id>", methods=["GET", "POST"])
def edit_destination(destination_id):
    destination = get_destination(destination_id)

    if request.method == "GET":
        return render_template("edit.html", destination=destination)

    if request.method == "POST":
        if destination["user_id"] != session["user_id"]:
            flash("VIRHE: Ei oikeuksia muokata kohdetta")
            return redirect("/edit/" + str(destination_id))

        csrf_token = request.form.get("csrf_token")
        if csrf_token != session.get("csrf_token"):
            flash("VIRHE: CSRF-virhe")
            return redirect("/edit/" + str(destination_id))

        description = request.form["description"]
        update_destination(destination["destination_id"], description)
        return redirect("/destinations/" + str(destination["destination_id"]))

@app.route("/remove_destination/<int:destination_id>", methods=["GET", "POST"])
def remove_trip_destination(destination_id):
    destination = get_destination(destination_id)

    if request.method == "GET":
        return render_template("remove_destination.html", destination=destination)

    if request.method == "POST":
        if destination["user_id"] != session["user_id"]:
            flash("VIRHE: Ei oikeuksia muokata kohdetta")
            return redirect("/remove_destination/" + str(destination_id))

        if "continue" in request.form:
            csrf_token = request.form.get("csrf_token")
            if csrf_token != session.get("csrf_token"):
                flash("VIRHE: CSRF-virhe")
                return redirect("/remove_destination/" + str(destination_id))
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
        flash("VIRHE: Käyttäjää ei löytynyt")
        return redirect("/")
    
    user_destinations = get_destinations_by_user(user_id)
    stats = get_user_stats(user_id)

    return render_template("user.html", user=user, destinations=user_destinations, stats=stats)

@app.route("/add_comment/<int:destination_id>", methods=["POST"])
def add_comment_route(destination_id):
    if "user_id" not in session:
        return redirect("/login")
    
    csrf_token = request.form.get("csrf_token")
    if csrf_token != session.get("csrf_token"):
        flash("VIRHE: CSRF-virhe")
        return redirect(f"/destinations/{destination_id}")

    user_id = session["user_id"]
    comment = request.form["comment"]

    add_comment(destination_id, user_id, comment)

    return redirect(f"/destinations/{destination_id}")

@app.route("/remove_comment/<int:comment_id>", methods=["GET", "POST"])
def remove_comment_route(comment_id):
    comment = get_comment(comment_id)

    if comment is None:
        flash("VIRHE: Kommenttia ei löytynyt")
        return redirect("/")

    destination_id = comment["destination_id"]

    if request.method == "GET":
        return render_template("remove_comment.html", comment=comment)

    if request.method == "POST":
        if comment["user_id"] != session["user_id"]:
            flash("VIRHE: Ei oikeuksia muokata kohdetta")
            return redirect("/remove_comment/" + str(comment_id))

        if "continue" in request.form:

            csrf_token = request.form.get("csrf_token")
            if csrf_token != session.get("csrf_token"):
                flash("VIRHE: CSRF-virhe")
                return redirect("/remove_comment/" + str(comment_id))

            remove_comment(comment["comment_id"])
        return redirect("/destinations/" + str(destination_id))
