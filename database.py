from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)

# Sql
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///MyRecipeList.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200))
    password = db.Column(db.String(200))

    def __init__(self, username, password):
        self.username = username
        self.password = password


class UserSchema(ma.ModelSchema):
    class Meta:
        model = User
