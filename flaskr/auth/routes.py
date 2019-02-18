import functools

from flask import (
    g, session, redirect, render_template, url_for, request, flash
)

from werkzeug.security import (
    check_password_hash, generate_password_hash
)

from flaskr.db import get_db

from . import bp 

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@bp.route("/register", methods=('GET', 'POST'))
def register():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        db = get_db()

        error = None

        if not username:
            error = "Username is required."
        elif len(username) > 8:
            error = "Username length has to be maximum 8 characters."
        elif not password:
            error = 'Password is required.'
        elif db.execute(
            'SELECT id FROM user WHERE username=?', (username,)
        ).fetchone() is not None:
            error = "User {} is already registed.".format(username)

        if error is None:
            db.execute(
                'INSERT INTO user (username, password)'
                ' VALUES (?, ?)',
                (username, generate_password_hash(password))
            )
            db.commit() 
            return redirect(url_for('auth.login'))

        flash(error)
    
    return render_template("auth/register.html")

@bp.route("/login", methods=('GET', 'POST'))
def login():
    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        db = get_db()

        error = None

        user = db.execute(
            'SELECT * FROM user WHERE username=?', (username,)
        ).fetchone()

        if user is None:
            error = "Incorrect username."
        elif not check_password_hash(user['password'], password):
            error = "Incorrect password."

        if error is None:
            session.clear() 
            session['user_id'] = user['id']
            return redirect(url_for('index'))
        
        flash(error)

    return render_template("auth/login.html")