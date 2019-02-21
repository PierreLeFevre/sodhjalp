import os
import re

from jinja2 import evalcontextfilter, Markup, escape
from flask import Flask

def create_app(host, port, test_config=None):
    app = Flask(__name__, instance_relative_config=True, template_folder='templates')
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
    )

    app.config['SERVER_NAME'] = "0.0.0.0:" + host.get("SERVER_PORT")
    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    from . import db
    db.init_app(app)

    from .auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    from .blog import bp as blog_bp
    app.register_blueprint(blog_bp)
    app.add_url_rule('/', endpoint='index')

    from .admin import bp as admin_bp
    app.register_blueprint(admin_bp)

    return app

    