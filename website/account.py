from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from .model import mysql
from .auth import login_required, session
from datetime import date, datetime

account=Blueprint('account', __name__)

def changePassword(email, password):
    try:
        cur = mysql.connection.cursor()
        cur.execute("UPDATE users passwrd = %s WHERE email = %s", (password, email))
        result = cur.fetchone()
        mysql.connection.commit()
        if result.row_count == 1:
            return 1
        return 0
    except Exception as e:
        print(f"Error: ${e}")
    
def changeEmail(email):
    try:
        cur = mysql.connection.cursor()
        cur.execute("UPDATE users email = %s", (email,))
        mysql.connection.commit()
        cur.close()
    except Exception as e:
        print(f"Error: ${e}")
        
@account.route('/account')
@login_required
def account_page():
    return render_template('account.html')

@account.route("/acc_signout")
@login_required
def signout():
    session.pop("user", None)
    return redirect(url_for('views.home_page'))

@account.route("/acc_get_info", methods=["POST"])
@login_required
def getInfo():
    email = session["user"]

    data = {
        'email': email
    }
    return jsonify(data)
