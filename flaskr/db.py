import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext

from werkzeug.security import (
    check_password_hash, generate_password_hash
)

def get_db():
        if "db" not in g:
                g.db = sqlite3.connect(
                        database=current_app.config["DATABASE"],
                        detect_types=sqlite3.PARSE_DECLTYPES
                )
                g.db.row_factory = sqlite3.Row

        return g.db

def close_db(e=None):
        db = g.pop("db", None)

        if db is not None:
                db.close()

def init_db():
        db = get_db()

        with current_app.open_resource("schema.sql") as f:
                db.executescript(f.read().decode('utf8'))

def create_robin_account():
        db = get_db()

        db.execute(
                'INSERT INTO user (username, password, is_teacher)'
                ' VALUES (?, ?, ?)', ("Robin", generate_password_hash("ntig123!"), 1)
        )

        db.commit()

def create_admin():
    db = get_db()
    db.execute(
        'INSERT INTO user (username, password, is_teacher, is_admin)'
        ' VALUES (?, ?, ?, ?)',
        ("Admin", generate_password_hash("ntig123!"), 1, 1)
    )

    db.commit()

def create_news():
    db = get_db()

    with current_app.open_resource('news.sql') as f: 
        db.executescript(f.read().decode('utf8'))

@click.command('create-news')
@with_appcontext
def init_news():
    create_news()
    click.echo('News table has been created')

@click.command('create-admin')
@with_appcontext
def init_db_admin():
    create_admin()
    click.echo('Admin account has been created.')


@click.command("init-db")
@with_appcontext
def init_db_command():
        init_db()
        click.echo("Initialized the database.")

@click.command("create-robin")
@with_appcontext
def init_db_command_robin():
        create_robin_account()
        click.echo("Robins accounts has been created.")


def init_app(app):
        app.teardown_appcontext(close_db)
        app.cli.add_command(init_db_command)
        app.cli.add_command(init_db_command_robin)
        app.cli.add_command(init_db_admin)
        app.cli.add_command(init_news)
