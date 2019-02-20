import datetime

from . import bp

from flaskr.db import get_db

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
        id = g.user['personal_id']
        week = current_week = datetime.datetime.now().isocalendar()[1]
        day = datetime.datetime.now().day
        url = '<img src="http://www.novasoftware.se/ImgGen/schedulegenerator.aspx?format=png&schoolid=80080/sv-se&id=' + id + '&period=&week=' + week + '&mode=0&day=' + day + '&width=300&height=600" class="img-fluid" alt="Schedule" id="schedule">'

        return url
    return dict(get_schedule_url=get_schedule_url)
