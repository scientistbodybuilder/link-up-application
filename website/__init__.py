from flask import Flask
from .model import init_db
import os

def create_app():
    app = Flask(__name__)
    app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
    app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
    app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
    app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    mysql = init_db(app)

    from .views import views
    from .auth import auth
    from .order import order
    from .linktree import linktree

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(order, url_prefix='/')
    app.register_blueprint(linktree, url_prefix='/')

    return app