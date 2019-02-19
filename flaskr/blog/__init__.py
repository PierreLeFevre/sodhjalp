from flask import Blueprint, g

from flaskr.auth.utils import login_required
from flaskr.db import get_db

bp = Blueprint("blog", __name__)


from . import routes, context_processors, utils