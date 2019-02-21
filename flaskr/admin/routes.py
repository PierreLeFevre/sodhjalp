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
		elif not password:
			error = "Password is required"
		elif len(password) < 8:
			error = "Password length needs to be greater than 8 characters"
		elif not email:
			error = "Email is required"
		elif not personal_id:
			error = "personalID is required"

		if error is not None:
			flash(error)
		else:
			db = get_db()
			db.execute(
				'UPDATE user SET username = ?, password = ?, email = ?, personal_id = ? WHERE id=?',
				(username, generate_password_hash(password), email, personal_id, id)
			)

			db.commit()
			return redirect(url_for('admin.index'))
	return render_template("admin/update.html", user=user)



