import functools

from flask import Blueprint, g

bp = Blueprint('auth', __name__, url_prefix="/auth")

from . import routes, before_request, utils