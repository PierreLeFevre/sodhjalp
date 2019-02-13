from flask import session, redirect, url_for, render_template, request

from werkzueg.security import generate_password_hash, \
        check_password_hash
        
from . import main
from ..database import mysql

import hashlib

@main.route("/")
def index():
    return render_template("index.html")

@main.route("/login", methods=["POST", "GET"])
def login():
    if (request.method == "POST"):

        username = request.sod_username
        password = hashlib.new(request.sod_password)

        cur = mysql.get_db().cursor()            
        result = cur.execute("SELECT * FROM Accounts WHERE username=%s AND password=%s", [username, password])

        #Credit does not match with a account
        if (result < 1):
            return redirect(url_for("login.html"))

        #Account succesfully login in
        return redirect(url_for("dashboard.html"))
    
    else if (request.method == "GET"):
        return render_template("login.html")
    
    else:
        return render_template("404.html")

@main.route("/register", methods=["POST", "GET"])
def register():
    if (request.method == "POST"):

        username = request.sod_username
        password = hashlib.new(request.sod_password)
        email = request.sod_email

        date = ""

        cur = mysql.get_db().cursor()
        result = cur.execute("SELECT * FROM Accounts WHERE username=%s AND password=%s", [username, password])

        #Account already exist
        if (result > 0):
            return redirect(url_for("register.html"))
        
        #Create a account
        result = cur.execute("INSERT INTO Accounts VALUES (%s, %s, %s)", [username, password, email, date])
        if (result > 1):
            return redirect(url_for("dashboard.html"))

        #Error with creating account
        return redirect(url_for("error.html"))

