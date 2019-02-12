import sys, os

from flask import Flask

from .database import mysql

def create_app(debug=False):

    app = Flask(__name__)
    app.debug = debug
    app.config["SECRET_KEY"] = os.urandom(24)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    app.config["MYSQL_HOST"] = "localhost"
    app.config["MYSQL_USER"] = "root"
    app.config["MYSQL_PASSWORD"] = "BoAs2879123123123"
    app.config["MYSQlQ_DB"] = "test"
    app.config["MYSQL_CURSORCLASS"] = "DictCursor"
    
    mysql.init_app(app) 

    return app

