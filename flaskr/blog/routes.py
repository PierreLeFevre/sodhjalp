from flask import (
    flash, g, redirect, render_template, request, url_for
)

from werkzeug.exceptions import abort

from flaskr.auth.utils import login_required
from flaskr.db import get_db

from .utils import (
    get_post,
    get_all_posts,
    search_posts,
    get_comment
)

from . import bp

@bp.route("/")
def index():
    posts = get_all_posts()
    return render_template('blog/index.html', posts=posts)

@bp.route("/search/<string:key>", methods=('GET', 'POST'))
def specific_posts(key = None):
    error = None

    if request.method == 'POST':
        posts = search_posts(request.form['search'])
        
        if len(posts) < 1:
            error = "Din sökning om {0} gav inga resultat.".format(request.form['search'])

        if error is not None:
            flash(error)
        else:
            return render_template('blog/index.html', posts=posts)

    posts = search_posts(key)
    return render_template('blog/index.html', posts=posts)




@bp.route("/create", methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        topic = request.form['class']
        error = None

        if not title:
            error = 'Title is required'
        elif topic == 'Välj...':
            error = 'Topic is required'
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

@bp.route("/<int:id>/update_comment", methods=('GET', 'POST'))
@login_required
def update_comment(id):

    comment = get_comment(id)

    if request.method == 'POST':
        body = request.form['body']
        error = None

        if not body:
            error = "Body is required."

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE comment SET body = ?'
                ' WHERE id = ?',
                (body, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))
    return render_template('blog/update_comment.html', comment=comment)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id) 
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))

@bp.route("/<int:id>/delete_comment", methods=('POST',))
@login_required
def delete_comment(id):
    get_comment(id)
    db = get_db()
    db.execute('DELETE FROM comment WHERE id = ?', (id,))
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