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
    get_user_data,
    get_all_feedbacks
)

from . import bp
import datetime

@bp.context_processor
def utility_processor_feedbacks():
	def get_feedback_user(id):
		user = get_db().execute(
			'SELECT * FROM user'
			' WHERE id=?',
			(id,)
		).fetchone()

		return user
	return dict(get_feedback_user=get_feedback_user)


@bp.context_processor
def utility_processor_schema():
    def get_schedule_url():
        id = str(g.user['personal_id'])
        week = str(datetime.datetime.now().isocalendar()[1])
        day = str(2**datetime.datetime.now().weekday())
        url = 'http://www.novasoftware.se/ImgGen/schedulegenerator.aspx?format=png&schoolid=80080/sv-se&id=' + id + '&period=&week=' + week + '&mode=0&day=' + day + '&width=300&height=600'

        return url
    return dict(get_schedule_url=get_schedule_url)

@bp.route("executeSQL", methods=('POST',))
@login_required
@be_admin
def sql():
	if (request.method == 'POST'):
		q = request.form['code']

		db = get_db()
		try:
			data = db.execute(q).fetchall()
			display_data = ""
			for row in data:
				display_data += {0}.format("".join(['{}'.format(col) for col in row])) + "\n"

			display_data += "\n"

			db.commit()
			flash("Code executed.", "success")
		except Exception as e:
			flash(e, "danger")

		return redirect(url_for('admin.index', data=display_data))

@bp.route("/")
@login_required
@be_admin
def index():
    users = get_all_users()
    feedbacks = get_all_feedbacks()
    return render_template('admin/index.html', users=users, feedbacks=feedbacks)

@bp.route("/<int:id>/update_password", methods=('GET', 'POST'))
@be_admin
@login_required
def update_password(id):
	user = get_user_data(id)

	if request.method == "POST":
		password = request.form['password']
		re_password = request.form['re_password']

		error = None

		if not password:
			error = "Password is required"
		elif not re_password:
			error = "Please type password again"
		elif password != re_password:
			error = "Passwords does not match"

		if error is not None:
			flash(error, 'danger')
		else:
			db = get_db()
			db.execute(
				'UPDATE user SET password = ?'
				' WHERE id = ?', (generate_password_hash(password), id)
			)
			db.commit()
			return redirect(url_for('admin.index'))
	return render_template('admin/update_password.html', user=user)

@bp.route("/<int:id>/update", methods=('GET', 'POST'))
@be_admin
@login_required
def update(id):
	user = get_user_data(id)

	if request.method == 'POST':
		username = request.form['username']
		email = request.form['email']
		personal_id = request.form['personal_id']

		is_admin = request.form.get('is_admin')
		is_teacher = request.form.get('is_teacher')

		if is_teacher is not None:
			is_teacher = 1
		else:
			is_teacher = 0

		if is_admin is not None:
			is_admin = 1
		else:
			is_admin = 0

		error = None

		if not username:
			error = "Username is required"

		if error is not None:
			flash(error, "danger")
		else:
			db = get_db()

			db.execute(
				'UPDATE user SET username = ?, email = ?, personal_id = ?, is_admin = ?, is_teacher = ? WHERE id=?',
				(username, email, personal_id, is_admin, is_teacher, id)
			)

			db.commit()
			return redirect(url_for('admin.index'))
	return render_template("admin/update.html", user=user)



