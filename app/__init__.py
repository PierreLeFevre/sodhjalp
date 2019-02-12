import sys, os

from flaskext.mysql import MySQL
from flask import Flask, g

from .database import mysql

def create_app(debug=False):

    app = Flask(__name__)
    app.debug = debug
    app.config["SECRET_KEY"] = os.urandom(24)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    app.config["MYSQL_DATABASE_HOST"] = "localhost"
    app.config["MYSQL_DATABASE_USER"] = "admin"
    app.config["MYSQL_DATABASE_PASSWORD"] = "password123"
    app.config["MYSQL_DATABASE_DB"] = "mydatabase" 

    mysql.init_app(app)

    return app

