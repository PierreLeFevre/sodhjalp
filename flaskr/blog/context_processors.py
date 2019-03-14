import datetime

from . import bp

from flaskr.db import get_db
from flask import g, flash

@bp.context_processor
def utility_processor_spam():
    def spam_detector(id):
        db = get_db()
        time = db.execute(
            'SELECT * as "datetime [times FROM post and comment'
            ' WHERE author_id=?',
            (g.user['id'])
        ).fetchone()

        return time

    return dict(spam_detector=spam_detector)

@bp.context_processor
def utility_processor_get_comments_order():
    def get_comments_amount(id, amount):
        db = get_db()
        comments = db.execute(
            'SELECT c.body, c.created, u.username, c.id, c.author_id'
            ' FROM comment c JOIN user u ON c.author_id=u.id'
            ' WHERE c.post_id=?'
            ' LIMIT ?', (id, amount)
        ).fetchall()

        return comments
    return dict(get_comments_amount=get_comments_amount)

@bp.context_processor
def utility_processor():
    def get_all_comments(id):

        db = get_db()
        comments = db.execute(
            'SELECT c.body, c.created, u.username, c.id, c.author_id'
            ' FROM comment c JOIN user u ON c.author_id=u.id'
            ' WHERE c.post_id=?', (id,)
        ).fetchall()

        return comments
    return dict(get_all_comments=get_all_comments)

@bp.context_processor
def utility_processor_remove_news():
    def remove_news(id):

        if (g.user['is_admin']):

            db = get_db()
            db.execute('DELETE FROM news WHERE id = ?', (id,))
            db.commit()
            flash('Removed news with id = {0}'.format(id))
            return redirect(url_for('blog.index'))
        flash('Failed to remove news with id = {0}'.format(id))
    return dict(remove_news=remove_news)

#@bp.context_processor
def utility_processor_posts():
    def get_posts_order(n):
        posts = get_db().execute(
            'SELECT * post'
            ' ORDER BY created DESC'
        ).fetchall()

@bp.context_processor
def utility_processor_user():
	def get_user(id):
	    user = get_db().execute(
	        'SELECT * FROM user WHERE id = ?', (id,)
	    ).fetchone()
	    
	    return user
	return dict(get_user = get_user)

@bp.context_processor
def utility_processor_schema():
    def get_schedule_url():
        id = str(g.user['personal_id'])
        week = str(datetime.datetime.now().isocalendar()[1])
        day = str(2**datetime.datetime.now().weekday())
        url = 'http://www.novasoftware.se/ImgGen/schedulegenerator.aspx?format=png&schoolid=80080/sv-se&id=' + id + '&period=&week=' + week + '&mode=0&day=' + day + '&width=300&height=450'

        return url
    return dict(get_schedule_url=get_schedule_url)
