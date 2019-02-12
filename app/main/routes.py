from flask import session, redirect, url_for, render_template, request

from . import main
from ..database import mysql

@main.route("/render")
def test():
    return render_template("index.html")

@main.route("/")
def index():

    cur = mysql.get_db().cursor()

    result = cur.execute("SELECT * FROM tbl")

    return str(cur.fetchall()[0])
