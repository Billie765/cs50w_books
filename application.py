import os
from flask import Flask, session, render_template, request, jsonify
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
    return render_template('home.html')
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

@app.route("/api/<string:isbn>", methods=["GET"])
def return_data(isbn):
    book = db.execute("SELECT * from books where isbn=:isbn", {'isbn':isbn}).fetchone()
    if book is None:
        return "Sorry, book not found", 404
    else:
        d = {'isbn': book.isbn, 'author': book.author, 'title': book.title, 'year': book.year}
        return jsonify(d)

@app.route("/search", methods=["GET","POST"])
def search():
    if request.method == "GET":
        return render_template('search.html')
    if request.method == 'POST':
        isbn = request.form.get("isbn")
        author = request.form.get("author")
        title = request.form.get("title")
        querry = f"SELECT * from books where isbn like '%{isbn}%' and author like '%{author}%' and title like '%{title}%'"
        results = db.execute(querry).fetchall()
        return render_template("result.html", isbn=isbn, author=author, title=title, results=results)

@app.route("/book/<string:isbn>")
def book(isbn):
    book = db.execute("SELECT * FROM books where isbn=:isbn", {'isbn':isbn}).fetchone()
    return render_template('book.html', title=book.title, author=book.author, isbn=book.isbn, year=book.year)
