from flask import Flask

app = Flask(__name__)

@app.route("/")
def index():
    return "root"

@app.route('/register', methods=['POST'])
def register():
    pass

@app.route('/login', methods=['POST'])
def login():
    pass

@app.route("/destinations", methods=["GET"])
def destinations():
    pass