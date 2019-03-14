import os
import re

from flask import Flask, request, render_template, flash
from flask_wtf.csrf import CSRFProtect, CSRFError

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True, template_folder='templates')
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"),
    )

    CSRFProtect(app)

    app.config['RECAPTCHA_USE_SSL'] = False
    app.config['RECAPTCHA_PUBLIC_KEY'] = 'public'
    app.config['RECAPTCHA_PRIVATE_KEY'] = 'private'
    app.config['RECAPTCHA_OPTIONS'] = {'theme': 'white'}

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

    @app.context_processor
    def utility_processor_remove_news():
        def remove_news(id):

            if (g.user['is_admin']):

                db = get_db
                db.execute('DELETE FROM news WHERE id = ?', (id,))
                db.commit()
                flash('Removed news with id = {0}'.format(id))
                return redirect(url_for('blog.index'))
            flash('Failed to remove news with id = {0}'.format(id))
        return dict(remove_news=remove_news)

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('error/404.html'), 404

    @app.errorhandler(CSRFError)
    def CSRFhandler(e):
        return render_template('error/csrf.html')

    return app

    