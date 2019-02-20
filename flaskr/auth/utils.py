import functools

from flask import (
    redirect, url_for, g, flash
)

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)

    return wrapped_view

def be_admin(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user['is_admin'] is 0:
            flash("Permission denied.")
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view