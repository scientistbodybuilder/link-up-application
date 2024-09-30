from flask import Blueprint, render_template, redirect, url_for
from .model import mysql
from .auth import login_required, session


order=Blueprint('order', __name__)

def validOrder():
    pass

@order.route('/order')
@login_required
def order_page():
    return render_template('order.html')

@order.route("/order_signout")
@login_required
def signout():
    session.pop("user", None)
    return redirect(url_for('views.home_page'))

@order.route('/place-order')
@login_required
def makeAnOrder():
    pass