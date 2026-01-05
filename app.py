import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

# Configure application
app = Flask(__name__)

# Enable debug mode for auto-reload (works with both flask run and python app.py)
app.config["DEBUG"] = True
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///civicpulse.db")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"

    # prevent caching of static files (CSS, JS, etc.)
    if response.content_type and 'text/css' in response.content_type:
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response

@app.route("/")
def index():
    
    return render_template("index.html")

@app.route('/register' , methods=["GET", "POST"])
def register():
    return render_template('register.html')

@app.route('/login' , methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "GET" :
        return render_template("login.html")

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        #Validate username --Ensure fields not empty--
        if not username or username.strip() == "":
            return render_template("login.html" , error = "Invalid Username")
        #Validate password
        if not password or password.strip() =="":
            return render_template("login.html" , error = "Invalid Password")

        rows = db.execute("SELECT * FROM users WHERE username = ?", (username,))

        if len(rows) != 1 or not check_password_hash(rows[0]["hash"],password):
            return render_template("login.html", error = "Invalid Username or Password")

        session["user_id"] = rows[0]["id"]
        session["role"] = rows[0]["role"]
        session["district"] = rows[0]["district"]

        return redirect("/")


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect("/")



    