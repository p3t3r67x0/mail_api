#!/usr/bin/env python3

from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_restful import Api
from flask_bcrypt import Bcrypt


app = Flask(__name__, static_folder=None)
app.config.from_pyfile('.config')

bcrypt = Bcrypt(app)
mail = Mail(app)
jwt = JWTManager(app)
api = Api(app, prefix='/api/v1')
db = SQLAlchemy(app)
