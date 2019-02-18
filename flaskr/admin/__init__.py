from flask import Blueprint, g

from flaskr.auth.utils import login_required
from flaskr.db import get_db

bp = Blueprint("admin", __name__)

from . import routes, utils