import os
import flask
from sqlalchemy import create_engine
from sqlalchemy.sql import text
from sqlalchemy.orm import sessionmaker, scoped_session
from flask import Flask, render_template, request, session, redirect
from flask_session import Session
from user import *

users = []
users.append(User(user_id="Roy", password="1111"))

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        user_id = request.form.get("user_id")
        password = request.form.get("user_password")

        user = db.execute(text("""SELECT * FROM users WHERE user_id = :user_id"""), {"user_id":user_id}).fetchone()

        if user and user.password == password:
            session['user_id'] = user.user_id
            return redirect("/book")
        return render_template("index.html", message="wrong id or password")
    return render_template("index.html")


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/register/result", methods=["POST"])
def register_result():

    new_id = request.form.get("user_id")
    new_password = request.form.get("user_password")

    # check if the user id exist in our database
    duplicate = db.execute(text("SELECT * FROM users WHERE user_id = :new_id"), {"new_id": new_id}).fetchone()

    # this is a new account
    if duplicate is None:
        db.execute(text("""INSERT INTO users (user_id, password)
                            VALUES(:new_id, :new_password)"""),
                   {"new_id": new_id, "new_password": new_password})
        db.commit()

        return render_template("registerresult.html")

    # the account already exists
    else:
        return render_template("register.html", message="The account already exist")


@app.route("/logout", methods=["POST", "GET"])
def logout():
    session.pop('user_id')
    return redirect("/")


@app.route("/book", methods=['GET', 'POST'])
def main_page():
    search_result = []

    if request.method == "GET":
        return render_template("mainpage.html", book=search_result)

    else:
        input_type = request.form.get("type")
        input_value = "%" + request.form.get("value") + "%"

        if input_type == "author":
            search_result = db.execute(text("""SELECT * FROM books
                                                    WHERE author_id IN
                                                    (SELECT id FROM authors
                                                    WHERE name LIKE :name)"""), {"name": input_value}).fetchall()
        else:
            search_result = db.execute(text("SELECT * FROM books "
                                            "WHERE " + input_type + " LIKE :input_value"),
                                       {"input_value": input_value}).fetchall()

        if len(search_result) == 0:
            return render_template("error.html", message="Nothing Match")
        else:
            return render_template("mainpage.html", books=search_result)


@app.route("/book/<string:isbn>")
def book_detail(isbn):
    print(isbn)
    detail = db.execute(text("""SELECT b.isbn, b.title, au.name, b.year
                                FROM books AS b, authors AS au
                                WHERE b.isbn =:isbn AND b.author_id = au.id"""),
                        {"isbn": isbn}).fetchone()
    print(detail)
    if len(detail) == 0:
        return render_template("error.html", message="Cannot find the details of the book")
    else:
        return render_template("detail.html", detail=detail)