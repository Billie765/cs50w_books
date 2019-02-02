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
        if db.execute("SELECT * from users WHERE login = :login",{"login":login}).rowcount == 0:
            return render_template("error.html", message="No such user")
            #return render_template("end.html", login = login, password=password)
        else:
            result = db.execute("SELECT password from users where login = :login", {'login':login}).fetchone()[0]
            if password == result:
                return render_template("success.html", message="You logged in")
            else:
                return render_template("error.html", message=f"login: {login}. password: {password}. result: {result}")
    else:
        return render_template("login.html")
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        login = request.form.get("login")
        password = request.form.get("password")
        if db.execute("SELECT * from users where login=:login", {'login':login}).rowcount == 0:
            db.execute("INSERT into users (login, password) VALUES (:login, :password)", {'login':login, 'password':password})
            db.commit()
            return render_template("success.html", message="Congrats")
        else:
            return render_template("error.html", message="User with this login already exists")
    else:
        return render_template("register.html")
