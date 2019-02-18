from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint("blog", __name__)

@bp.context_processor
def utility_processor():
    def get_all_comments(id):

        db = get_db()
        comments = db.execute(
            'SELECT c.body, c.created, u.username, u.id, c.author_id'
            ' FROM comment c JOIN user u ON c.author_id=u.id'
            ' WHERE c.post_id=?', (id,)
        ).fetchall()

        return comments
    return dict(get_all_comments=get_all_comments)

@bp.route('/')
def index():
    posts = get_all_posts()

    return render_template('blog/index.html', posts=posts)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        topic = request.form['class']
        error = None

        if not title:
            error = 'Title is required.'
        elif topic == "Välj...":
            error = "Topic is required."
        elif not body:
            error = "Question is required"
        
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id, topic)'
                ' VALUES (?, ?, ?, ?)',
                (title, body, g.user['id'], topic)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create.html')

def get_post(id, check_author=True):
    post = get_db().execute(
        'SELECT p.id, p.topic, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if post is None:
        abort(404, "Post id {0} doesn't exist.".format(id))

    if g.user['is_teacher'] == 1:
        return post
        
    if check_author and post['author_id'] != g.user['id']:
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


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/update.html', post=post)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))

@bp.route("/<int:id>/create_comment", methods=("GET", "POST"))
@login_required
def create_comment(id):

    post = get_post(id, check_author=False)

    if request.method == "POST":
        body = request.form["body"]
        error = None

        if not body:
            error = "Body is required"

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO comment (body, author_id, post_id)'
                ' VALUES (?, ?, ?)',
                (body, g.user['id'], id)
            )
            db.commit()
            return redirect(url_for('blog.index'))

    return render_template('blog/create_comment.html', post=post)