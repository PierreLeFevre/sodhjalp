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