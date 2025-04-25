from flask_sqlalchemy import SQLAlchemy


# mysql = MySQL()


# def init_db(app):
#     mysql.init_app(app)
#     return mysql
from datetime import datetime

db = SQLAlchemy()

import os
from supabase import create_client, Client
url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(url, key)

class Users(db.Model):
    user_id = db.Column(db.Integer, primary_key=True, unique=True)
    email = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    organization = db.Column(db.String(200), nullable=True, unique=True)
    link_tree_card = db.Column(db.Integer, default=0)
    direct_card = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'User <{self.email}>'

class Cards(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    organization = db.Column(db.String(200), db.ForeignKey('users.organization'), nullable=True,default=None)
    link_tree_card = db.Column(db.Integer, default=0)
    direct_card = db.Column(db.Integer, default=0)
    first_order_date = db.Column(db.Date, nullable=True, default=None)
    email = db.Column(db.String(200), db.ForeignKey('users.email'), unique=True, nullable=False)

    def __repr__(self):
        return f'<Cards of {self.email}>'

class Orders(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    order_id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    amount = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), db.ForeignKey('users.email'), nullable=False)
    order_date = db.Column(db.String(200), nullable=True)
    LT_card = db.Column(db.Integer)
    D_card = db.Column(db.Integer)

    def __repr__(self):
        return f'<Orders of {self.user_id}>'

