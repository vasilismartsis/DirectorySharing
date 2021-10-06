from flask import Blueprint, render_template, request, session, url_for
from database import *
from getDirectories import *

logout = Blueprint("logout", __name__, static_folder="static",
                   template_folder="templates")


@logout.route("/")
def logoutAction():
    session.clear()
    return getDirectories()
