from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/register', methods=['GET, POST'])
def register():
    pass

@app.route('/login', methods=['GET, POST'])
def login():
    pass

@app.route("/destinations", methods=["GET"])
def destinations():
    pass