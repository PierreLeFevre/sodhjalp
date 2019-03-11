import functools

from flask import (
    g, session, redirect, render_template, url_for, request, flash
)

from werkzeug.security import (
    check_password_hash, generate_password_hash
)

from ..admin.utils import (
    get_all_users
)

from .utils import (
    login_required
)

from flaskr.db import get_db

from . import bp 

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@login_required
@bp.route("/settings", methods=('GET', 'POST'))
def settings():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        re_password = request.form['re_password']
        email = request.form['email']
        personal_id = request.form['personal_id']
    
        error = None

        if username is None:
            error = "Username is required"
        elif len(username) > 8:
            error = "Username length needs to be less than 8 characters"
        elif len(password) < 8 and len(password) > 0:
            error = "Password length needs to be greater than 8 characters"
        elif password != re_password:
            error = "Passwords does not match"

        check_dub = get_db().execute(
            'SELECT * FROM user WHERE LOWER(username)=LOWER(?)', (username,) 
        ).fetchone()

        if check_dub is not None and g.user['username'].lower() != username.lower():
            error = "Username already exist"

        if error is not None:
            flash(error, "danger")
        else:
            db = get_db()
                
            if len(password) < 1:
                db.execute(
                    'UPDATE user SET username = ?, personal_id = ?'
                    ' WHERE id = ?', (username, personal_id, g.user['id'])
                )
            else:
                db.execute(
                    'UPDATE user SET username = ?, password = ?, personal_id = ?'
                    ' WHERE id = ?', (username, generate_password_hash(password), personal_id, g.user['id'])
                )

            if len(email) > 1:
                db.execute(
                    'UPDATE user SET email = ?'
                    ' WHERE id = ?', (email, g.user['id'])
                )

            


            db.commit()
            return redirect(url_for('blog.index'))
    return render_template('auth/settings.html')

@bp.route("/register", methods=('GET', 'POST'))
def register():

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        re_password = request.form['re_password']

        db = get_db()

        error = None

        if not username:
            error = "Username is required."
        elif len(username) > 8:
            error = "Username length has to be maximum 8 characters."
        elif not password:
            error = 'Password is required.'
        elif not re_password:
            error = "Please re type your password"
        elif password != re_password:
            error = "Password does not match"
        elif db.execute(
            'SELECT id FROM user WHERE username=?', (username,)
        ).fetchone() is not None:
            error = "User {} is already registed.".format(username)

        if error is None:
            db.execute(
                'INSERT INTO user (username, password, email, personal_id)'
                ' VALUES (?, ?, ?, ?)',
                (username, generate_password_hash(password), email, personal_id)
            )
            db.commit() 
            return redirect(url_for('auth.login'))

        flash(error, "danger")
    
    return render_template("auth/register.html")

@bp.route("/login", methods=('GET', 'POST'))
def login():
    if request.method == 'POST':

        username = request.form['username'].lower()
        password = request.form['password']

        db = get_db()

        error = None

        user = db.execute(
            'SELECT * FROM user WHERE LOWER(username)=?', (username,)
        ).fetchone()

        if user is None:
            error = "Incorrect username."
        elif not check_password_hash(user['password'], password):
            error = "Incorrect password."

        if error is None:
            session.clear() 
            session['user_id'] = user['id']
            return redirect(url_for('index'))
        
        flash(error, "danger")

    return render_template("auth/login.html")