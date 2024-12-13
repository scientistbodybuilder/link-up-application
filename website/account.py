from flask import Blueprint, render_template, redirect, url_for, request, jsonify, flash
from werkzeug.security import generate_password_hash, check_password_hash
from .model import Users, Cards, Orders, db
from .auth import login_required, session, User, contains_num, checkPassword, checkEmail
from datetime import date, datetime

account=Blueprint('account', __name__)
m = ""

def getOrderHistory(id):
    # cur = mysql.connection.cursor()
    l=[]
    try:
        # cur.execute("SELECT * FROM orders WHERE user_id = %s", (id,))
        # result = cur.fetchall()
        # cur.close()
        orders = Orders.query.filter_by(user_id=id)
        for row in orders:
            order = {
                'date':row.order_date,
                'LTcard': row.LT_card,
                'Dcard': row.D_card,
                'total': row.amount
            }
            l.append(order)
        return l

    except Exception as e:
        print(f"Error: {e}")
        return l
    

def getUser(email):
    # cur = mysql.connection.cursor()
    try:
        # cur.execute("SELECT * FROM cards WHERE email = %s",(email,))
        # result = cur.fetchone()
        row = Cards.query.filter_by(email=email).first()
        user = User(email,"",row.link_tree_card,row.direct_card)
        user.user_id = session["id"]
        # cur.close()
        return user
    except Exception as e:
        print(f"Error: ${e}")

def changePassword(email, password):
    try:
        # cur = mysql.connection.cursor()
        # cur.execute("UPDATE users SET passwrd = %s WHERE email = %s", (generate_password_hash(password), email))
        # result = cur.fetchone()
        # mysql.connection.commit()
        # cur.close()
        user = Users.query.filter_by(email=email).first()
        if user:
            user.password = password
            db.session.commit()
            print('PASSWORD UPDATED')
            return 1
        print('USER NOT FOUND')
        return 0
    except Exception as e:
        print(f"Error: ${e}")

def verifyPassword(email, password):
    # cur = mysql.connection.cursor()
    try:
        # cur.execute("SELECT passwrd FROM users WHERE email = %s",(email,))
        # result = cur.fetchone()
        user = Users.query.filter_by(email=email)
        if check_password_hash(user.password, password):
            return 1
        else:
            return 0

    except Exception as e:
        print(f"Error: ${e}")
    
def changeEmail(id,new_email):
    try:
        # cur = mysql.connection.cursor()
        # cur.execute("UPDATE users SET email = %s WHERE user_id = %s", (new_email,id))
        # mysql.connection.commit()
        # cur.close()
        user = Users.query.filter_by(user_id=id)
        if user:
            user.email = new_email
            db.session.commit()
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
        return jsonify({"page": url_for('account.edit_page')})
    else:
        m = "email"
        print(f"request to change email, and m = {m}")
        password = data['check_password']
        if verifyPassword(password):
            return jsonify({"page": url_for('account.edit_page')})
        else:
            flash("Incorrect Password")
    return render_template('account.html')

@account.route("/edit_page",methods=['GET','POST'])
@login_required
def edit_page():
    if request.method == 'POST':
        field = request.form['field']
        print(f"the field is {field}")
        confirm_field = request.form['confirm-field']
        print(f"the confirm field is {confirm_field}")
        if m == "email":
            x = checkEmail(field, confirm_field)
            if x:
                id = session["id"]
                changeEmail(id,field)
                return redirect(url_for('auth.logout'))
            elif x ==2:
                flash("Enter a valid email")
            else:
                flash("Emails do not match")
        else:
            x = checkPassword(field, confirm_field)
            print(f"check password on {field} is {x}")
            if x==1:
                changePassword(session["user"],field)
                return redirect(url_for('auth.logout'))
            elif x==2:
                flash("Password must be atleast 7 characters long")
            elif x ==3:
                flash("Passwords do not match")
            else:
                flash("Password must contain a number")
    
    if m == "password":
        return render_template('editform.html', prompt = "Password")
    return render_template('editform.html', prompt = "Email")

@account.route("/update_info",methods=['GET','POST'])
@login_required
def updateInfo():
    field = request.form['field']
    confirm_field = request.form['confirm-field']
    if m == "email":
        x = checkEmail(field, confirm_field)
        if x:
            id = session["id"]
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

@account.route("/order-history", methods=['POST'])
@login_required
def showHistory():
    id = session['id']
    l = getOrderHistory(id)
    result = [{'date': order['date'], 'LTcard': order['LTcard'], 'Dcard':order['Dcard'], 'total':order['total']} for order in l]
    print(result)
    return jsonify(result)
