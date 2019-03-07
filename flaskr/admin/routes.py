from flask import (
    flash, g, redirect, render_template, request, url_for
)

from werkzeug.exceptions import abort

from flaskr.auth.utils import login_required, be_admin
from flaskr.db import get_db

from werkzeug.security import (
    check_password_hash, generate_password_hash
)

from .utils import (
    get_all_users,
    get_user_data
)

from . import bp
import datetime

@bp.context_processor
def utility_processor_schema():
    def get_schedule_url():
        id = str(g.user['personal_id'])
        week = str(datetime.datetime.now().isocalendar()[1])
        day = str(2**datetime.datetime.now().weekday())
        url = 'http://www.novasoftware.se/ImgGen/schedulegenerator.aspx?format=png&schoolid=80080/sv-se&id=' + id + '&period=&week=' + week + '&mode=0&day=' + day + '&width=300&height=600'

        return url
    return dict(get_schedule_url=get_schedule_url)


@bp.route("/")
@login_required
@be_admin
def index():
    users = get_all_users()
    return render_template('admin/index.html', users=users)

@bp.route("/<int:id>/update", methods=('GET', 'POST'))
@be_admin
@login_required
def update(id):
	user = get_user_data(id)

	if request.method == 'POST':
		username = request.form['username']
		password = request.form['password']
		email = request.form['email']
		personal_id = request.form['personal_id']

		error = None

		if not username:
			error = "Username is required"
		elif not password and len(password) > 0:
			error = "Password is required"
		elif len(password) < 8 and len(password) > 0:
			error = "Password length needs to be greater than 8 characters"
		elif not email:
			error = "Email is required"
		elif not personal_id:
			error = "personalID is required"

		if error is not None:
			flash(error)
		else:
			db = get_db()

			if (len(password) > 0):

				db.execute(
					'UPDATE user SET username = ?, email = ?, personal_id = ? WHERE id=?',
					(username, email, personal_id, id)
				)
			else:
				db.execute(
					'UPDATE user SET username = ?, password = ?, email = ?, personal_id = ? WHERE id=?',
					(username, generate_password_hash(password), email, personal_id, id)
				)

			db.commit()
			return redirect(url_for('admin.index'))
	return render_template("admin/update.html", user=user)



