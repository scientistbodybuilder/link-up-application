from flask import Blueprint, render_template, session, redirect, url_for
from .model import mysql
from .auth import login_required, session


order=Blueprint('order', __name__)

@order.route('/order')
@login_required
def order_page():
    return render_template('order.html')