from flask import Blueprint, render_template, request, session
from database import *
from werkzeug.security import generate_password_hash, check_password_hash
from getDirectories import *

login = Blueprint("login", __name__, static_folder="static",
                  template_folder="templates")


@login.route("/")
def loginPage():
    return render_template("index.html", content="login")


@login.route("/checkUser", methods=["POST", "GET"])
def checkUser():
    if "username" not in session:
        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]

            if username and password:
                found_user = User.query.filter_by(username=username).first()
                found_user = UserSchema(many=False).dump(found_user)
                if found_user:
                    if(check_password_hash(found_user["password"], password)):
                        session["username"] = username
                        return getDirectories()
                    else:
                        return render_template("index.html", content="login", status="passwordNotCorrect")
                else:
                    return render_template("index.html", content="login", status="userNotFound")
        else:
            return render_template("index.html", content="login")
    else:
        return render_template("index.html", content="login")
