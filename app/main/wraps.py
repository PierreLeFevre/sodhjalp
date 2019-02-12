from flask import flash
from functools import wraps

def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if False:
            return f(*args, **kwargs)
        else:
            flash("Works!")
            return redirect(url_for("login"))
    return wrap
