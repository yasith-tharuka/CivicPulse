import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps

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


def login_required(f):
    """
    Decorate routes to require login.
    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

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

        return redirect(url_for("dashboard"))



@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect("/")

@app.route('/register' , methods = ["GET","POST"])
def register():
    if request.method == "GET":
        return render_template("register.html", errors={}, username="", district="")
    if request.method == "POST":
        errors = {}

        username = request.form.get("username")
        district = request.form.get("district")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Username validation
        if not username:
            errors["username"] = "Invalid Username"

        # District validation
        valid_districts = [
            "Colombo", "Galle", "Kandy", "Matara", "Jaffna",
            "Kurunegala", "Anuradhapura", "Badulla", "Ratnapura", "Trincomalee",
            "Batticaloa", "Hambantota", "Monaragala", "Polonnaruwa", "Puttalam",
            "Nuwara Eliya", "Ampara", "Mannar", "Kilinochchi", "Vavuniya",
            "Mullaitivu", "Matale", "Kalutara", "Gampaha", "Kegalle"
        ]
        if district not in valid_districts:
            errors["district"] = "Please Select A District From Dropdown"

        # Password validation
        if not password:
            errors["password"] = "Invalid Password"
        elif password != confirmation:
            errors["confirmation"] = "Password Not Matching"

        # Check if username already exists (only if username is provided)
        if username:
            rows = db.execute("SELECT * FROM users WHERE username = ?", (username,))
            if len(rows) != 0:
                errors["username"] = "Username already in Use"

        # If errors exist, re-render form
        if errors:
            return render_template("register.html", errors=errors, username=username or "", district=district or "")

        # Hash password
        hash_pw = generate_password_hash(password) 

        # Save data into 'civicpulse.db' database 'users' table 
        # CS50 SQL library returns the row ID directly from INSERT
        # Pass parameters as separate arguments (not as a tuple)
        user_id = db.execute(
            "INSERT INTO users (username, hash, district, role) VALUES (?, ?, ?, ?)",
            username, hash_pw, district, "citizen")

        # Set session variables (similar to login)
        session["user_id"] = user_id
        session["role"] = "citizen"
        session["district"] = district
        
        return redirect(url_for("dashboard"))


        
@app.route("/dashboard")
@login_required
def dashboard():
    """Show the dashboard"""
    
    # Get current user details from session
    user_id = session["user_id"]
    role = session["role"]
    district = session["district"]

    # LOGIC: 
    # If Official -> See ALL reports in their district
    # If Citizen -> See ONLY reports they submitted
    if role == "official":
        incidents = db.execute(
            "SELECT incidents.* FROM incidents JOIN users ON incidents.user_id = users.id WHERE users.district = ? ORDER BY incidents.timestamp DESC",
            (district,))
    else:
        incidents = db.execute("SELECT * FROM incidents WHERE user_id = ? ORDER BY timestamp DESC", (user_id,))

    return render_template("dashboard.html", incidents=incidents)





