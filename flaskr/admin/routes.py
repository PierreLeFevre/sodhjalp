from flask import (
    flash, g, redirect, render_template, request, url_for
)

from werkzeug.exceptions import abort

from flaskr.auth.utils import login_required, be_admin
from flaskr.db import get_db

from .utils import (
    get_all_users
)

from . import bp

@bp.route("/")
@login_required
def index():
    users = get_all_users()
    return render_template('admin/index.html', users=users)

    