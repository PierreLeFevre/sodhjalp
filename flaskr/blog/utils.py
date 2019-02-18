from flask import g

from flaskr.db import get_db

def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, p.topic, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    if check_author and post['author_id'] != g.user['id']:
        abort(403)

    if g.user['is_teacher'] == 0:
        abort(403)

    return post

def get_all_posts():
    db = get_db()
    posts = db.execute(
        'SELECT p.id, p.topic, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()

    return posts

def search_posts(key):
    db = get_db()

    posts = db.execute(
        'SELECT p.id, p.topic, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id=u.id'
        ' WHERE p.topic=? OR p.title=? OR body=? OR username=? OR created=?', (key, key, key, key, key)
    ).fetchall()

    return posts

    