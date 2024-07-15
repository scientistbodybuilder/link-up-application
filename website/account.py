from flask import Blueprint, render_template, redirect, url_for, request, jsonify, flash
from werkzeug.security import generate_password_hash, check_password_hash
from .model import mysql
from .auth import login_required, session, User, contains_num, checkPassword, checkEmail
from datetime import date, datetime

account=Blueprint('account', __name__)
m = ""

def getUserId(email):
    cur = mysql.connection.cursor()
    try:   
        cur.execute("SELECT user_id FROM users WHERE email = %s",(email,))
        result = cur.fetchone()
        cur.close()
        return result[0]
    except Exception as e:
        print(f"Error: ${e}")

def getUser(email):
    cur = mysql.connection.cursor()
    try:
        cur.execute("SELECT * FROM cards WHERE email = %s",(email,))
        result = cur.fetchone()
        user = User(email,"",result[2],result[3])
        user.user_id = getUserId(email)
        cur.close()
        return user
    except Exception as e:
        print(f"Error: ${e}")

def changePassword(email, password):
    try:
        cur = mysql.connection.cursor()
        cur.execute("UPDATE users passwrd = %s WHERE email = %s", (generate_password_hash(password), email))
        result = cur.fetchone()
        mysql.connection.commit()
        cur.close()
        if result.row_count == 1:
            return 1
        return 0
    except Exception as e:
        print(f"Error: ${e}")

def verifyPassword(email, password):
    cur = mysql.connection.cursor()
    try:
        cur.execute("SELECT passwrd FROM users WHERE email = %s",(email,))
        result = cur.fetchone()
        if check_password_hash(result[0], password):
            return 1
        else:
            return 0

    except Exception as e:
        print(f"Error: ${e}")
    
def changeEmail(id,new_email):
    try:
        cur = mysql.connection.cursor()
        cur.execute("UPDATE users email = %s WHERE user_id = %s", (new_email,id))
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
    user = getUser(email)

    data = {
        'email': email,
        'direct_card': user.D_card,
        'linktree_card': user.LT_card
    }
    # print(data['direct_card'])
    # print(data['linktree_card'])
    return jsonify(data)

@account.route("/render_edit_page",methods=['GET','POST'])
@login_required
def render_form():
    global m
    data = request.get_json()
    if data['form'] == "password":
        m = "password"
        print(f"request to change password, and m = {m}")
        return render_template('editform.html', prompt = "Password")
    else:
        print(f"request to change email, and m = {m}")
        password = data['check_password']
        if verifyPassword(password):
            m = "email"
            return render_template('editform.html', prompt = "Email")
        else:
            flash("Incorrect Password")

@account.route("/update_info",methods=['GET','POST'])
@login_required
def updateInfo():
    field = request.form['field']
    confirm_field = request.form['confirm-field']
    if m == "email":
        x = checkEmail(field, confirm_field)
        if x:
            old_email = session["user"]
            id = getUserId(old_email)
            changeEmail(id,field)
            return redirect(url_for('auth.logout'))
        elif x ==2:
            flash("Enter a valid email")
        else:
            flash("Emails do not match")
    else:
        x = checkPassword(field, confirm_field)
        if x:
            changePassword(session["user"],field)
            return redirect(url_for('auth.logout'))
        elif x==2:
            flash("Password must be atleast 7 characters long")
        elif x ==3:
            flash("Passwords do not match")
        else:
            flash("Password must contain a number")