from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from .auth import login_required, session

linktree=Blueprint('linktree', __name__)

@linktree.route('/OzzyBurgers')
def ozzyBurger():
    return render_template('OzzyBurger.html')

# @linktree.route('/OzzyBurgers')
# def ozzyBurger():
#     return render_template('OzzyBurger.html')


# @linktree.route('/OzzyBurgers')
# def ozzyBurger():
#     return render_template('OzzyBurger.html')


# @linktree.route('/OzzyBurgers')
# def ozzyBurger():
#     return render_template('OzzyBurger.html')


