from flask import (
    flash, g, redirect, render_template, request, url_for
)

import datetime
import calendar
import time as t

from werkzeug.exceptions import abort

from flaskr.auth.utils import (
    login_required,
    be_admin
)

from flaskr.db import get_db

from .utils import (
    get_post,
    get_all_posts,
    search_posts,
    get_comment,
    get_news,
    get_posts
)

from . import bp

@bp.route("/<int:id>/remove_news", methods=('GET',))
@be_admin
@login_required
def remove_news(id):

    db = get_db()
    db.execute('DELETE FROM news WHERE id = ?', (id,))
    db.commit()
    flash('Removed news with id = {0}'.format(id), "success")
    return redirect(url_for('blog.index'))

@bp.route("/create_news", methods=('GET', 'POST'))
@login_required
@be_admin
def news():

    news = get_news()

    if request.method == 'POST':

        title = request.form['title']
        body = request.form['body']
        pic = request.form['pic']

        error = None

        if len(title) > 50:
            error = "Title needs to be less than 50 characters"
        elif len(body) > 200:
            error = "Body needs to be less than 200 characters"

        if error is not None:
            flash(error, "danger")
        else:

            if pic is None:
                pic = "None"

            db = get_db()
            db.execute(
                'INSERT INTO news (title, body, pic, author_id)'
                ' VALUES (?, ?, ?, ?)',
                (title, body, pic, g.user['id'])
            )

            db.commit()
            flash("News has been created", "success")
            return redirect(url_for('blog.index'))

    return render_template('blog/create_news.html', news=news)


#@bp.route("/test/test")
def test():
    db = get_db()
    time = db.execute(
        'SELECT * FROM post'
        ' WHERE author_id=?',
        (g.user['id'],)
    ).fetchone()

    date, time = str(time['created']).split(" ")

    #Checking if its the same date.
    if (str(date) == str(datetime.date.today())):
        
        return str((t.strftime("%H:%M:%S")) - int(time))

    return str(datetime.date.today())

@bp.route("/")
def index():
    posts = get_all_posts()
    news = get_news()
    return render_template('blog/index.html', posts=posts, news=news    )

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

@bp.route("/<string:username>/profile", methods=('GET', 'POST'))
@login_required
def profile(username):

    posts = get_posts(username)

    return render_template('blog/profile.html', posts=posts)

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
            epoch = calendar.timegm(t.gmtime())
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