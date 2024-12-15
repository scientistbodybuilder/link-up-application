from flask import Flask
from .model import db
from flask_sqlalchemy import SQLAlchemy
import os


# db = SQLAlchemy()
def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql://link_db_zqe3_user:NR6TGDCi5IUTa5TpaGCUBHK5jqZDPKCL@dpg-ctf6rf0gph6c73fkca80-a.ohio-postgres.render.com/link_db_zqe3')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
    # app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
    # app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
    # app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    # app.config['MAIL_SERVER'] = "smtp.gmail.com"
    # app.config['MAIL_PORT'] = 465
    # app.config['MAIL_USERNAME'] = "suspiciousemail54@gmail.com"
    # app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    # app.config['MAIL_USE_TLS'] = False
    # app.config['MAIL_USE_SSL'] = True

    db.init_app(app)
    # mysql = init_db(app)

    from .views import views
    from .auth import auth
    from .order import order
    from .linktree import linktree
    from .account import account

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(order, url_prefix='/')
    app.register_blueprint(linktree, url_prefix='/')
    app.register_blueprint(account, url_prefix='/')

    return app