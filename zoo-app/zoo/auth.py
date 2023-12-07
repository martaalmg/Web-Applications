from flask import Blueprint, render_template, request, redirect, url_for, flash
from . import db, bcrypt
import flask_login
from . import model

bp = Blueprint("auth", __name__)


@bp.route("/signup")
def signup():
    return render_template("auth/signup.html")

@bp.route("/signup", methods=["POST"])
def signup_post():
    email = request.form.get("email")
    username = request.form.get("username")
    password = request.form.get("password")
    roleStr = request.form.get("Role")

    if roleStr == "Client":
        role = True
    else:
        role = False
    managerCode = request.form.get("managerCode")

   # Check that the manager code is correct (123)
    if managerCode != "123" and role==False: 
        flash("The manager code is wrong" )
        return redirect(url_for("auth.signup")) 

    # Check that passwords are equal
    if password != request.form.get("password_repeat"):
        flash("Sorry, passwords are different")
        return redirect(url_for("auth.signup"))

    # Check if the email is already at the database
    user = model.User.query.filter_by(email=email).first()
    if user:
        flash("Sorry, the email you provided is already registered")
        return redirect(url_for("auth.signup"))

    password_hash = bcrypt.generate_password_hash(password).decode("utf-8")
    new_user = model.User(email=email, name=username, password=password_hash, role = role)
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for("auth.login"))

@bp.route("/login")
def login():
    return render_template("auth/login.html")

@bp.route("/login", methods=["POST"])
def login_post():
    email = request.form.get("email")
    password = request.form.get("password")

    # Get the user with that email from the database:
    user = model.User.query.filter_by(email=email).first()

    if user and bcrypt.check_password_hash(user.password, password) and user.role==1:  # COMPLETAR  
        # The user exists and the password is correct and you are a client
        flask_login.login_user(user)
        return redirect(url_for("main.homepage"))

    elif user and bcrypt.check_password_hash(user.password, password) and user.role==0: # COMPLETAR
        # The user exists and the password is correct and you are a manager
        flask_login.login_user(user)
        return redirect(url_for("main.homepage"))     
         
    else:
        flash("Wrong email and/or password")
        return redirect(url_for("auth.login"))

@bp.route("/logout")
def logout():
    flask_login.logout_user()  
    return redirect(url_for("main.homepage"))
