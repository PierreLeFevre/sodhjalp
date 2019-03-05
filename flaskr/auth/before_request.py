from flask import g, session

from flaskr.db import get_db
import datetime


from . import bp

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

@bp.context_processor
def utility_processor_schema():
    def get_schedule_url():
        id = str(g.user['personal_id'])
        week = str(datetime.datetime.now().isocalendar()[1])
        day = str(2**datetime.datetime.now().weekday())
        url = 'http://www.novasoftware.se/ImgGen/schedulegenerator.aspx?format=png&schoolid=80080/sv-se&id=' + id + '&period=&week=' + week + '&mode=0&day=' + day + '&width=300&height=600'

        return url
    return dict(get_schedule_url=get_schedule_url)
