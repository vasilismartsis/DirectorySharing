from flask import Flask, redirect, url_for, render_template, request, jsonify, make_response, Blueprint, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from account import account
from database import *
from getDirectories import *

app.register_blueprint(account, url_prefix="/account")

app.secret_key = "mySecretKey"

scheduler = BackgroundScheduler()


@app.route("/", methods=["GET", "POST"])
def index():
    return getDirectories()


@app.route('/download')
def download():
    return send_from_directory(request.args.get('previousPath'), request.args.get('fileName'), as_attachment=True)


@app.route('/upload')
def upload():
    return send_from_directory(request.args.get('previousPath'), request.args.get('fileName'))


if __name__ == "__main__":
    db.create_all()
    app.debug = True
    app.run(host='0.0.0.0', port=5005, use_reloader=True)
