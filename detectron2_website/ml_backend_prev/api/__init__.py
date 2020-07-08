from flask import Flask
import os

def create_app():
    print ("Hello")
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

    # from .ml import ml_blueprint
    # app.register_blueprint(ml_blueprint, url_prefix="/ml")

    @app.route("/")
    def index():
    	return "Index"

    return app
