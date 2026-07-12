import math
import time

from urllib.parse import urlencode
from flask import Flask, render_template, request, session, redirect, flash, g

import markupsafe
import config
import destinations
import users
import comments

app = Flask(__name__)
app.secret_key = config.SECRET_KEY

@app.route("/")
@app.route("/<int:page>")
def index(page=1):
    page_size = 10
    destination_count = destinations.destination_count()
    page_count = math.ceil(destination_count / page_size)
    page_count = max(page_count, 1)

    if page < 1:
        return redirect("/1")
    if page > page_count:
        return redirect("/" + str(page_count))

    all_destinations = destinations.get_destinations(page, page_size)
    categories = destinations.get_categories()

    filled = {arg: request.args[arg] for arg in ["name", "description"] if arg in request.args}

    return render_template(
        "index.html", 
        page=page,
        page_count=page_count,
        destinations=all_destinations,
        categories=categories,
        filled=filled
    )

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html", filled={})

    username = request.form["username"].strip()
    password1 = request.form["password1"]
    password2 = request.form["password2"]

    if not username or not password1:
        flash("VIRHE: Ei syötettä")
        return render_template("register.html", filled={"username": username})
    if len(username) > 50 or len(password1) > 128:
        flash("VIRHE: Liian pitkä syöte")
        return render_template("register.html", filled={"username": username})
    if password1 != password2:
        flash("VIRHE: Salasanat eivät ole samat")
        return render_template("register.html", filled={"username": username})

    if users.register_user(username, password1):
        return redirect("/")

    flash("VIRHE: Tunnus on jo varattu")
    return render_template("register.html", filled={"username": username})

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html", filled={})

    username = request.form["username"].strip()
    password = request.form["password"]

    if not username or not password:
        flash("VIRHE: Ei syötettä")
        return render_template("login.html", filled={"username": username})
    if len(username) > 50 or len(password) > 128:
        flash("VIRHE: Liian pitkä syöte")
        return render_template("login.html", filled={"username": username})

    if users.login_user(username, password):
        return redirect("/")

    flash("VIRHE: Väärä tunnus tai salasana")
    return render_template("login.html", filled={"username": username})

@app.route("/logout")
def logout():
    users.logout_user()
    return redirect("/")

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

    if not name or not description:
        flash("VIRHE: Ei syötettä")
        return redirect(f"/?{urlencode({"description": description})}")
    if len(name) > 75 or len(description) > 5000:
        flash("VIRHE: Liian pitkä syöte")
        return redirect(f"/?{urlencode({"description": description})}")

    categories = []
    for entry in request.form.getlist("categories"):
        if entry:
            parts = entry.split(":")
            categories.append((parts[0], parts[1]))

    destination_id = destinations.add_destination(name, description, user_id, categories)
    return redirect("/destinations/" + str(destination_id))

@app.route("/destinations/<int:destination_id>")
def show_destination(destination_id):
    destination = destinations.get_destination(destination_id)
    categories = destinations.get_destination_categories(destination_id)
    all_comments = comments.get_comments(destination_id)
    return render_template(
        "destination.html", 
        destination=destination,
        categories=categories,
        comments=all_comments
    )

@app.route("/edit/<int:destination_id>", methods=["GET", "POST"])
def edit_destination(destination_id):
    destination = destinations.get_destination(destination_id)

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

        if not description:
            flash("VIRHE: Ei syötettä")
            return redirect("/edit/<int:destination_id>")
        if len(description) > 5000:
            flash("VIRHE: Liian pitkä syöte")
            return redirect("/edit/<int:destination_id>")

        destinations.update_destination(destination["destination_id"], description)
        return redirect("/destinations/" + str(destination["destination_id"]))

@app.route("/remove_destination/<int:destination_id>", methods=["GET", "POST"])
def remove_trip_destination(destination_id):
    destination = destinations.get_destination(destination_id)

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
            destinations.remove_destination(destination["destination_id"])
        return redirect("/")

@app.route("/search")
def search_results():
    query = request.args.get("query")
    results = destinations.search(query) if query else []
    return render_template("search.html", query=query, results=results)

@app.route("/users/<int:user_id>")
def user_profile(user_id):
    user = users.get_user(user_id)
    if not user:
        flash("VIRHE: Käyttäjää ei löytynyt")
        return redirect("/")

    user_destinations = destinations.get_destinations_by_user(user_id)
    stats = destinations.get_user_stats(user_id)

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

    if not comment:
        flash("VIRHE: Ei syötettä")
        return redirect(f"/destinations/{destination_id}")
    if len(comment) > 75:
        flash("VIRHE: Liian pitkä syöte")
        return redirect(f"/destinations/{destination_id}")

    comments.add_comment(destination_id, user_id, comment)

    return redirect(f"/destinations/{destination_id}")

@app.route("/remove_comment/<int:comment_id>", methods=["GET", "POST"])
def remove_comment_route(comment_id):
    comment = comments.get_comment(comment_id)

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

            comments.remove_comment(comment["comment_id"])
        return redirect("/destinations/" + str(destination_id))

@app.before_request
def before_request():
    g.start_time = time.time()

@app.after_request
def after_request(response):
    elapsed_time = round(time.time() - g.start_time, 2)
    print("elapsed time:", elapsed_time, "s")
    return response

@app.template_filter()
def show_lines(content):
    content = str(markupsafe.escape(content))
    content = content.replace("\n", "<br />")
    return markupsafe.Markup(content)
