import os
from flask import Flask, session, render_template, request
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    return "Project 1: TODO. What's next?"
@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        login = request.form.get("login")
        password = request.form.get("password")
        return render_template("end.html", login = login, password=password)
    else:
        return render_template("login.html")
'''@app.route("/<string:name>")
def name(name):
    return f"Hello, {name}"'''
