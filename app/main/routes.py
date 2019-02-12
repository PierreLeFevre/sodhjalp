from flask import session, redirect, url_for, render_template, request

from . import main
from ..database import mysql

@main.route("/")
def index():

    cur = mysql.get_db().cursor()

    result = cur.execute("SELECT * FROM users")

    return cur.fetchall()
