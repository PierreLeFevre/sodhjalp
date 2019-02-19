from flask import g

from flaskr.db import get_db

def get_all_users():

    users = get_db().execute(
        'SELECT * FROM user'
    ).fetchall()

    #Check if user is admin...

    return users

def get_user(id):

    db = get_db()
    user = db.execute(
        'SELECT * FROM user'
        ' WHERE id=?',
        (id,)
    ).fetchone()

    return user


