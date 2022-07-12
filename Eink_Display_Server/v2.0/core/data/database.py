import sqlite3
import click

from flask import current_app, g
from flask.cli import with_appcontext

def dbconnect():
    '''
    connect to app db, store in g.db
    '''
    
    if 'db' not in g:
        g.db= sqlite3.connect(
            current_app.config['DATABASE'], 
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory= sqlite3.Row
        
    return g.db

def dbclose(e= None):
    '''
    close current connection, dellocate g.db
    '''
    
    db = g.pop("db", None)
    if db is not None: db.close()

def dbinit():
    '''
    delete current and create new blank database
    '''
    
    db = dbconnect()
    with current_app.open_resource("static/dbschema.sql") as f:
        db.executescript(f.read().decode("utf8"))


@click.command("init-db")
@with_appcontext
def dbinit_command():
    '''
    init database with flask command
    usage: flask init-db
    '''
    
    dbinit()
    click.echo("Initialized the database.")


def appinit(app):
    '''
    Register database functions with the Flask app. This is called by
    the application factory.
    '''
    
    app.teardown_appcontext(dbclose)
    app.cli.add_command(dbinit_command)
