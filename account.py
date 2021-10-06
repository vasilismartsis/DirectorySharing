from flask import Blueprint, render_template
from database import *

from logout import logout
from login import login
from register import register

account = Blueprint("account", __name__, static_folder="static",
                    template_folder="templates")


app.register_blueprint(login, url_prefix="/login")
# app.register_blueprint(register, url_prefix="/register")
app.register_blueprint(logout, url_prefix="/logout")
