from flask import Blueprint, g

from flaskr.auth.utils import login_required
from flaskr.db import get_db

bp = Blueprint("admin", __name__, url_prefix="/admin/beta")

from . import routes, utils