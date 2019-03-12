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
    #posts = get_all_posts()
    return render_template('blog/index.html')

@bp.route("/search/<string:key>", methods=('GET', 'POST'))
def specific_posts(key = None):

    error = None

    if request.method == 'POST':
        posts = search_posts(request.form['search'])
        
        if len(posts) < 1:
            error = "Din sökning om {0} gav inga resultat.".format(request.form['search'])

        if error is not None:
            flash(error, "info")
        else:
            return render_template('blog/index.html', posts=posts)

    posts = search_posts(key)
    return render_template('blog/index.html', posts=posts)

@bp.route("/feedback", methods=('GET', 'POST'))
@login_required
def feedback():

    if request.method == 'POST':
        title = request.form['title'].lstrip()
        body = request.form['body'].lstrip()

        error = None

        if not title:
            error = 'Title is required'
        elif not body:
            error = 'Body is required'
        elif not len(body) < 500:
            error = "Length of body needs to be less than 500 characters"
        elif not len(title) < 100:
            error = "Length of title needs to be less than 100 characters"

        if error is not None:
            flash(error, "danger")
        else:
            db = get_db()
            db.execute(
                'INSERT INTO feedback (user_id, title, body)'
                ' VALUES (?, ?, ?)',
                (g.user['id'], title, body)
            )
            db.commit()
            flash("TANK YOU FUR YUOR FEDBAK", "success")

            return redirect(url_for('blog.index'))
    return render_template('blog/feedback.html')

@bp.route("/create", methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title'].lstrip()
        body = request.form['body'].lstrip()
        topic = request.form['class']
        error = None

        if not title:
            error = 'Title is required'
        elif topic == 'Välj...':
            error = 'Topic is required'
        elif not body:
            error = "Question is required" 
        elif not len(body) < 500:
            error = "Keep it short and sweet, maximum length is 500 characters on the body"
        elif not len(title) < 50:
            error = "Keep it short and sweet, maximum length is 50 characters on the title"

        if error is not None:
            flash(error, "danger")
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
        title = request.form['title'].lstrip()
        body = request.form['body'].lstrip()
        error = None

        if not title:
            error = 'Title is required.'
        elif not len(body) < 500:
            error = "Body length needs to be less than 500 characters"

        if error is not None:
            flash(error, "danger")
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
        body = request.form['body'].lstrip()
        error = None

        if not body:
            error = "Body is required."
        elif not len(body) < 500:
            error = "Body length needs to be less than 500 characters"

        if error is not None:
            flash(error, "danger")
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
    db.execute('DELETE FROM comment WHERE post_id = ?', (id,))
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

@bp.route("/<int:id>/post", methods=("GET", "POST"))
def show_post(id):

    post = get_post(id, check_author=False)
    return render_template('blog/show_post.html', post=post)

@bp.route("/<int:id>/create_comment", methods=("GET", "POST"))
@login_required
def create_comment(id):

    post = get_post(id, check_author=False)

    if request.method == "POST":
        body = request.form["body"].lstrip()
        error = None

        if not body:
            error = "Body is required"
        elif not len(body) < 500:
            error = "Body length needs to be maximum 500 characters"

        if error is not None:
            flash(error, "danger")
        else:
            db = get_db()
            db.execute(
                'INSERT INTO comment (body, author_id, post_id)'
                ' VALUES (?, ?, ?)',
                (body, g.user['id'], id)
            )
            db.commit()
            return redirect(url_for('blog.show_post', id=id))

    return render_template('blog/show_post.html', post=post)

@bp.route("/google3d59e7cfe1f46259.html")
def google():
    return render_template('google3d59e7cfe1f46259.html')