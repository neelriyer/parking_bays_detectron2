from flask import Flask
from flask_pymongo import PyMongo 
from flask_httpauth import HTTPBasicAuth
from celery import Celery
from config import config
import os


mongo = PyMongo()
auth = HTTPBasicAuth()
celery = Celery(__name__, broker=config['default'].CELERY_BROKER_URL)

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    mongo.init_app(app)
    celery.conf.update(app.config)

    from .ml import ml_blueprint
    app.register_blueprint(ml_blueprint, url_prefix="/ml")

    from .users import users_blueprint 
    app.register_blueprint(users_blueprint, url_prefix="/users")    

    from .errors import errorhandler_blueprint
    app.register_blueprint(errorhandler_blueprint)

    from .auth import verify_password

    return app
