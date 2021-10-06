from flask import Blueprint, render_template, request, session
from database import *
from werkzeug.security import generate_password_hash, check_password_hash

register = Blueprint("register", __name__, static_folder="static",
                     template_folder="templates")


@register.route("/")
def registerPage():
    return render_template("index.html", content="register")


@register.route("/addUser", methods=["POST", "GET"])
def addUser():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username and password:
            found_user = User.query.filter_by(username=username).first()
            if found_user:
                return render_template("index.html", content="register", status="usernameAlreadyExists")
            else:
                usr = User(username, generate_password_hash(password))
                db.session.add(usr)
                db.session.commit()
                session["username"] = username
                return render_template("index.html", content="register", status="success")
    else:
        return render_template("index.html", content="register")
