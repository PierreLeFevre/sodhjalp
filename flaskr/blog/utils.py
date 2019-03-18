from flask import g

import datetime

from werkzeug.exceptions import abort

from flaskr.db import get_db

from flask_wtf import FlaskForm, RecaptchaField
from wtforms import TextField

#Kan finnas säkerhets problem
def get_news():

    news = get_db().execute(
        'SELECT * FROM news'
        ' ORDER BY created DESC'
    ).fetchall()

    return news

def get_posts(username, check_author=True):

    posts = get_db().execute(
        'SELECT p.id, p.topic, p.title, p.body, p.created, p.author_id u.username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE LOWER(p.username) = ?'
        ' ORDER BY created',
        (username.lower(),)
    ).fetchall()

    if posts is None:
        abort(404, "Nothing was found")

    if check_author and (post['author_id'] != g.user['id'] or g.user['is_teacher'] or g.user['is_admin']):
        abort(403)

    return posts

def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, p.topic, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?'
        ' ORDER BY created',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    if check_author and (post['author_id'] != g.user['id'] or g.user['is_teacher'] == 0):
        abort(403)

    return post

def get_comment(id, check_author=True):
    comment = get_db().execute(
        'SELECT author_id, id, body FROM comment'
        ' WHERE id=?'
        ' ORDER BY created',
        (id,)
    ).fetchone()

    if comment is None:
        abort(404, "Comment id {0} doesn't exist.".format(id))

    if check_author and (comment['author_id'] != g.user['id'] or g.user['is_teacher'] == 0):
        abort(403)

    return comment

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

    key = key.lower()

    #CONVERT(column2 USING utf8)

    posts = db.execute(
        'SELECT p.id, p.topic, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id=u.id'
        ' WHERE instr(LOWER(p.topic), ?) OR instr(LOWER(title), ?) OR instr(LOWER(body), ?) OR instr(LOWER(created), ?) OR instr(LOWER(username), ?)'
        ' ORDER BY created DESC', (key, key, key, key, key)
    ).fetchall()

    return posts


#' WHERE CONTAINS(LOWER(p.topic), ?) OR CONTAINS(LOWER(title), ?) OR CONTAINS(LOWER(body), ?) OR CONTAINS(LOWER(created), ?) OR CONTAINS(LOWER(username), ?)', (key, key, key, key, key)
#' WHERE LOWER(p.topic) LIKE ? OR LOWER(p.title) LIKE ? OR LOWER(body) LIKE ? OR LOWER(username) LIKE ? OR LOWER(created) LIKE ?', (key, key, key, key, key)
