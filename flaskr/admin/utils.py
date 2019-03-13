from flask import g

from flaskr.db import get_db

def get_all_users():

    users = get_db().execute(
        'SELECT * FROM user'
    ).fetchall()

    #Check if user is admin...

    return users



def get_all_feedbacks():
    db  = get_db()
    feedbacks = db.execute(
        'SELECT * FROM feedback'
    ).fetchall()

    return feedbacks

def get_user_data(id):

    db = get_db()
    user = db.execute(
        'SELECT * FROM user'
        ' WHERE id=?',
        (id,)
    ).fetchone()

    return user


