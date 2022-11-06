import os
import re

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required
import json

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///ideas.db")

valid_email = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')

DEPARTMENTS = [
    "Finance",
    "Sales",
    "Marketing",
    "Operations",
    "Engineering",
    "Product",
    "Customer Experience",
    "Legal",
    "HR",
    "Other"
]

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/login", methods=["GET", "POST"])
def login():
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT id, hash FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["ID"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/register_company", methods=["GET", "POST"])
def register_company():
    """Register user"""
    if request.method == "POST":
        # collect info from form
        username = request.form.get("username")
        company = request.form.get("company")
        size = request.form.get("size")
        industry = request.form.get("industry")
        password = request.form.get("password")
        FirstName = request.form.get("firstname")
        LastName = request.form.get("lastname")
        email = request.form.get("email")
        department = request.form.get("department")
        confirmation = request.form.get("confirmation")
        password_hash = generate_password_hash(password)
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        emails = db.execute("SELECT email FROM users WHERE email = ?", email)
        companies = db.execute("SELECT * FROM users WHERE company = ?", company)

        # error check
        if not username:
            return apology("Username Required", 400)
        if not company or not size or not industry:
            return apology("Company Info missing", 400)
        if len(companies) == 1:
            return apology("Company already registered", 400)
        if not FirstName:
            return apology("First Name Required", 400)
        if not LastName:
            return apology("Last Name Required", 400)
        if not email:
            return apology("Email Required", 400)
        if not department:
            return apology("Department Required", 400)
        if len(rows) == 1:
            return apology("Username already exists", 400)
        if len(emails) >= 1:
            return apology("Email already exists", 400)
        if not re.fullmatch(valid_email, email):
            return apology("Invalid Email", 400)
        if not password:
            return apology("Password Required", 400)
        if len(password) < 8:
            return apology("Password must have at least 8 characters", 400)
        if not any(c.isdigit() for c in password):
            return apology("Password must contain numbers", 400)
        if not confirmation:
            return apology("Please re-enter password", 400)
        if not password == confirmation:
            return apology("Passwords do not match", 400)

        # if valid then update the user db
        db.execute("INSERT INTO users(username, hash, FirstName, LastName, email, department, permissions, company) VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
                   username, password_hash, FirstName, LastName, email, department, 'admin', company)
        db.execute("INSERT INTO companies(company, industry, size) VALUES(?, ?, ?)",
                   company, industry, size)
        # automatically login the user after they have registered
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        print(rows)
        session["user_id"] = rows[0]["ID"]
        print(session["user_id"])
        return redirect("/")
    else:
        return render_template("register_company.html", departments=DEPARTMENTS)

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        # ask the user for required info
        username = request.form.get("username")
        company = request.form.get("company")
        password = request.form.get("password")
        FirstName = request.form.get("firstname")
        LastName = request.form.get("lastname")
        email = request.form.get("email")
        department = request.form.get("department")
        confirmation = request.form.get("confirmation")
        password_hash = generate_password_hash(password)
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        emails = db.execute("SELECT email FROM users WHERE email = ?", email)
        companies = db.execute("SELECT * FROM users WHERE company = ?", company)

        # error check
        if not username:
            return apology("Username Required", 400)
        if not company:
            return apology("Company Required", 400)
        if len(companies) == 0:
            return render_template("registration_failed.html")
        if not FirstName:
            return apology("First Name Required", 400)
        if not LastName:
            return apology("Last Name Required", 400)
        if not email:
            return apology("Email Required", 400)
        if not department:
            return apology("Department Required", 400)
        if len(rows) == 1:
            return apology("Username already exists", 400)
        if len(emails) >= 1:
            return apology("Email already exists", 400)
        if not re.fullmatch(valid_email, email):
            return apology("Invalid Email", 400)
        if not password:
            return apology("Password Required", 400)
        if len(password) < 8:
            return apology("Password must have at least 8 characters", 400)
        if not any(c.isdigit() for c in password):
            return apology("Password must contain numbers", 400)
        if not confirmation:
            return apology("Please re-enter password", 400)
        if not password == confirmation:
            return apology("Passwords do not match", 400)

        # if valid then update the user db
        db.execute("INSERT INTO users(username, hash, FirstName, LastName, email, department, permissions, company) VALUES(?, ?, ?, ?, ?, ?, ?, ?)",
                   username, password_hash, FirstName, LastName, email, department, 'user', company)

        # automatically login the user after they have registered
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)
        print(rows)
        session["user_id"] = rows[0]["ID"]
        print(session["user_id"])
        return redirect("/")
    else:
        return render_template("register.html", departments=DEPARTMENTS)


@app.route("/")
@login_required
def index():
    # get user id
    id = session.get("user_id")
    # find users company
    rows = db.execute("SELECT company FROM users WHERE id = ?", id)
    company = rows[0]["company"]
    # query db for all ideas submitted for current company
    ideas = db.execute("SELECT * FROM ideas WHERE stage = ? AND company = ?", "idea", company)
    inReview = db.execute("SELECT * FROM ideas WHERE stage = ? AND company = ?", "review", company)
    accepted = db.execute("SELECT * FROM ideas WHERE stage = ? AND company = ?", "accept", company)
    rejected = db.execute("SELECT * FROM ideas WHERE stage = ? AND company = ?", "reject", company)
    return render_template("index.html", ideas=ideas, inReview=inReview, accepted=accepted, rejected=rejected)


@app.route("/vote")
@login_required
def ideas():
    #get user id
    id = session.get("user_id")
    # query db for all ideas submitted for current company
    rows = db.execute("SELECT company FROM users WHERE id = ?", id)
    company = rows[0]["company"]
    ideas = db.execute("SELECT * FROM ideas WHERE stage = ? AND company = ? ORDER BY title ASC", "idea", company)
    return render_template("vote.html", ideas=ideas)

@app.route("/upvote/<int:idea_id>")
def upvote(idea_id):
    # get user_id
    id = session.get("user_id")
    #Check if user has voted on idea before this
    actions = db.execute("SELECT action FROM actions WHERE idea_id = ? AND user_id = ?", idea_id, id)

    if len(actions) == 0:
        #get current upvotes from current idea and increase count by 1
        row = db.execute("SELECT upvotes FROM ideas WHERE idea_id = ?", idea_id)
        votes = int(row[0]["upvotes"])
        upvotes = votes + 1
        #update db with new upvotes
        db.execute("UPDATE ideas SET upvotes = ? WHERE idea_id = ?",upvotes, idea_id)
        #add action to actions db
        db.execute("INSERT INTO actions (idea_id, action, user_id) VALUES (?, ?, ?)",idea_id, "upvote", id)
        #if there's more than 10 votes then update stage
        if upvotes >= 10:
            db.execute("UPDATE ideas SET stage = ? WHERE idea_id = ? AND stage = ?",'review', idea_id, 'idea')
        return redirect("/vote")

    else:
        return render_template("voted.html")


@app.route("/downvote/<int:idea_id>")
def downvote(idea_id):
    # get user_id
    id = session.get("user_id")
    #Check if user has voted on idea before this
    actions = db.execute("SELECT action FROM actions WHERE idea_id = ? AND user_id = ?", idea_id, id)

    if len(actions) == 0:
        #get current upvotes from current idea and increase count by 1
        row = db.execute("SELECT downvotes FROM ideas WHERE idea_id = ?", idea_id)
        votes = int(row[0]["downvotes"])
        downvotes = votes - 1
        #update db with new upvotes
        db.execute("UPDATE ideas SET downvotes = ? WHERE idea_id = ?",downvotes, idea_id)
        #add action to actions db
        db.execute("INSERT INTO actions (idea_id, action, user_id) VALUES (?, ?, ?)",idea_id, "downvote", id)
        #if there's more than 10 votes then update stage
        if downvotes <= -5:
            db.execute("UPDATE ideas SET stage = ? WHERE idea_id = ? AND stage = ?",'rejected', idea_id, 'idea')
        return redirect("/vote")
    else:
        return render_template("voted.html")

@app.route("/idea_page/<int:idea_id>", methods=["GET", "POST"])
def idea_page(idea_id):
    if request.method == "POST":
        # get submitted comment and add to comments db
        print("POST")
        id = session.get("user_id")
        comment = request.form.get("comment")
        db.execute("INSERT INTO comments(comment, user_id, idea_id) VALUES(?, ?, ?)",
                   comment, id, idea_id)
        return redirect(url_for("idea_page", idea_id=idea_id))
    else:
        # get all idea info and comments for current idea
        id = session.get("user_id")
        ideas = db.execute("SELECT * FROM ideas WHERE idea_id = ?", idea_id)
        comments = db.execute("SELECT * FROM comments JOIN users ON comments.user_id = users.id WHERE comments.idea_id = ?", idea_id)
        # find users current permission and render relevant template based onn permissions
        rows = db.execute("SELECT permissions FROM users WHERE id = ?", id)
        permission = rows[0]["permissions"]
        stages = db.execute("SELECT stage FROM ideas WHERE idea_id = ?", idea_id)
        stage = stages[0]["stage"]
        if permission == "admin" and stage == "review":
            return render_template("decide.html", ideas=ideas, comments=comments, idea_id=idea_id)
        elif stage == "idea":
            return render_template("voting_page.html", ideas=ideas, idea_id=idea_id, comments=comments)
        else:
            return render_template("ideas_page.html", ideas=ideas, comments=comments, idea_id=idea_id)

@app.route("/accept/<int:idea_id>")
def accept(idea_id):
    print('idea_id')
    # find users permissions
    id = session.get("user_id")
    rows = db.execute("SELECT permissions FROM users WHERE id = ?", id)
    permission = rows[0]["permissions"]
    # if user is admin allow db to update idea stage
    if permission == "admin":
        db.execute("UPDATE ideas SET stage = ? WHERE idea_id = ?",
                'accept', idea_id)
    return redirect('/')

@app.route("/reject/<int:idea_id>")
def reject(idea_id):
    print('idea_id')
    # find user permissions
    id = session.get("user_id")
    rows = db.execute("SELECT permissions FROM users WHERE id = ?", id)
    permission = rows[0]["permissions"]
    # if user is an admin then allow db to update idea stage
    if permission == "admin":
        db.execute("UPDATE ideas SET stage = ? WHERE idea_id = ?",
                'reject', idea_id)
    return redirect('/')

@app.route("/history")
@login_required
def history():
    # select all actions current user has taken
    user_id = session.get("user_id")
    ideas = db.execute(
        "SELECT DISTINCT(ideas.title), ideas.time, actions.action FROM ideas JOIN actions ON ideas.idea_id = actions.idea_id WHERE ideas.user_id = ?",
        user_id)
    return render_template("history.html", ideas=ideas)


@app.route("/review", methods=["GET", "POST"])
@login_required
def review():
    if request.method == "POST":
        # get stage user wants to filter to
        stage = request.form.get("stage")
        print(stage)
        # if they haven't choosen a stage view all ideas
        if stage == 'Choose Stage':
            return redirect('/review')
        elif stage is None:
            return redirect('/review')
        # select ideas based on users selected stage
        else:
            stages = db.execute("SELECT DISTINCT(stage) FROM ideas")
            ideas = db.execute("SELECT * FROM ideas WHERE stage = ? ORDER BY title ASC", stage)
            return render_template("filter.html", ideas=ideas, stages=stages)
    else:
        # find user id and company
        id = session.get("user_id")
        rows = db.execute("SELECT company FROM users WHERE id = ?", id)
        company = rows[0]["company"]
        # select applicable idea stages for current company
        stages = db.execute("SELECT DISTINCT(stage) FROM ideas ORDER BY title ASC")
        # select all ideas submitted to current company
        ideas = db.execute("SELECT * FROM ideas WHERE company = ? ORDER BY title ASC", company)
        return render_template("ideas.html", ideas=ideas, stages=stages)


@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    if request.method == "POST":
        # check user id and current company
        id = session.get("user_id")
        rows = db.execute("SELECT company FROM users WHERE id = ?", id)
        company = rows[0]["company"]
        # get form data
        title = request.form.get("title")
        notes = request.form.get("notes")
        rows = db.execute("SELECT * FROM ideas WHERE title = ?", title)
        # error check
        if not title or not notes:
            return apology("Missing Input", 400)
        if len(rows) >= 1:
            return apology("Title already exists, please use another title", 400)
        # update ideas and actions
        db.execute("INSERT INTO ideas (user_id, title, notes, stage, company) VALUES (?, ?, ?, ?, ?)",
                   id, title, notes, "idea", company)
        row = db.execute("SELECT idea_id FROM ideas WHERE user_id = ? AND title = ?",
                         id, title)
        idea_id = row[0]["idea_id"]
        db.execute("INSERT INTO actions (idea_id, action, user_id) VALUES (?, ?, ?)",
                   idea_id, "submit", id)
        return render_template("submitted.html")
    else:
        return render_template("add.html", departments=DEPARTMENTS)

@app.route("/settings")
@login_required
def settings():
    # check user id
    id = session.get("user_id")
    # check user permissions
    rows = db.execute("SELECT permissions FROM users WHERE id = ?", id)
    permission = rows[0]["permissions"]
    # check user company
    rows = db.execute("SELECT company FROM users WHERE id = ?", id)
    company = rows[0]["company"]
    # select all users from current company
    users = db.execute("SELECT * FROM users WHERE company = ?", company)
    permissions = db.execute("SELECT DISTINCT(permissions) FROM users")
    if permission == "admin":
        return render_template("settings.html", users=users, permissions=permissions)
    else:
        return render_template("permissions.html")

@app.route("/update_permissions/<int:user_id>")
@login_required
def update_permissions(user_id):
    # check users persmissions
    permissions = db.execute("SELECT permissions FROM users WHERE ID = ?", user_id)
    permission = permissions[0]["permissions"]
    # if admin change to user
    if permission == 'admin':
        db.execute("UPDATE users SET permissions = ? WHERE ID = ?",'user', user_id)
    # if user change to admin
    else:
        db.execute("UPDATE users SET permissions = ? WHERE ID = ?",
                       'admin', user_id)
    return redirect("/settings")