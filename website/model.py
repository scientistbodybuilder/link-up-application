from flask_sqlalchemy import SQLAlchemy


# mysql = MySQL()


# def init_db(app):
#     mysql.init_app(app)
#     return mysql
from datetime import datetime

db = SQLAlchemy()

class Users(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    org_name = db.Column(db.String(200), nullable=True)

    cards = db.relationship('Cards', backref='user',lazy=True)
    orders = db.relationship('Orders', backref='user',lazy=True)

    def __repr__(self):
        return f'User <{self.email}>'

class Cards(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    org_name = db.Column(db.String(200), nullable=True,default=None)
    link_tree_card = db.Column(db.Integer, default=0)
    direct_card = db.Column(db.Integer, default=0)
    first_order_date = db.Column(db.Date, nullable=True, default=None)
    email = db.Column(db.String(200), unique=True)

    def __repr__(self):
        return f'<Cards of {self.email}>'

class Orders(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    order_id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    amount = db.Column(db.String(200), nullable=False)
    order_date = db.Column(db.String(200), nullable=True)
    LT_card = db.Column(db.Integer)
    D_card = db.Column(db.Integer)

    def __repr__(self):
        return f'<Orders of {self.user_id}>'

