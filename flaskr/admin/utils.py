from flask import g

from flaskr.db import get_db

def get_all_users():

    users = get_db().execute(
        'SELECT * FROM user'
    ).fetchall()

    #Check if user is admin...

    return users

