import os
from flask import Flask
from core import logging as log

threads = []

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping( 
        SECRET_KEY='thisisseriouspysecured',
        DATABASE=os.path.join(app.instance_path, 'bluetag.db'),
    )

    if test_config is None: app.config.from_pyfile('config.py', silent=True)
    else: app.config.update(test_config)

    # ensure the instance folder exists
    try: os.makedirs(app.instance_path)
    except OSError: pass

    # register the database commands
    from core.data import database as db
    db.appinit(app)

    # apply the blueprints to the app
    from api import auth as auth_api
    from api import slave as slave_api
    from api import system as sys_api
    from page import dashboard, slave, system, auth
    
    app.register_blueprint(auth_api.bp)
    app.register_blueprint(slave_api.bp)
    app.register_blueprint(sys_api.bp)
    
    app.register_blueprint(dashboard.bp)
    app.register_blueprint(slave.bp)
    app.register_blueprint(system.bp)
    app.register_blueprint(auth.bp)

    app.add_url_rule("/", endpoint="dashboard.index")
     
    log.event('API started')
    log.event('Site started')
    return app

def add_threads(item):
    threads.append(item)
    return threads

def remove_threads(item):
    threads.remove(item)
    return threads

def get_threads(mac = None):
    if mac != None:
        for x in threads:
            if x['mac'] == mac:
                thread = x
                return thread
    return threads

def init_threads():
    threads.clear()
    return threads