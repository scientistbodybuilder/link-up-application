from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from .model import mysql
from functools import wraps

auth=Blueprint('auth', __name__)

class User:
    def __init__(self,email,password,linktree_card, direct_card):
        self.email = email
        self.password = password
        self.LT_card = linktree_card
        self.D_card = direct_card
        self.user_id=""

def contains_num(s):
    for char in s:
        if char.isdigit():
            return True
    return False

def checkPassword(password, confirm_password):
    if len(password)<7:
            return 2
    elif password != confirm_password:
        return 3
    elif not contains_num(password):
        return 4
    return 1

def checkEmail(email, confirm_email):
    if not("@" in email or "." in email):
        return 2
    elif email != confirm_email:
        return 3
    return 1

def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for('auth.login_page'))
        return f(*args, **kwargs)
    return wrapper


def uniqueEmail(User):
    cur = mysql.connection.cursor()
    try:
        cur.execute("SELECT * FROM users WHERE email = %s", (User.email,))
        user = cur.fetchone()
        if user:
            print("user exist")
            print(user)
            return False
        else:
            return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def createUser(User):
    cur = mysql.connection.cursor()
    hashed_password = generate_password_hash(User.password, method='pbkdf2:sha256')
    try:
        cur.execute("INSERT INTO users (email,passwrd) VALUES (%s,%s)", (User.email,hashed_password))
        mysql.connection.commit()
        cur.close()
        if cur.rowcount == 1:
            return 1
        else:
            return 0
    except Exception as e:
            print(f"Error: {e}")
            return 0
    
def initializeCards(User):
    cur = mysql.connection.cursor()
    try:
        cur.execute("SELECT user_id FROM users WHERE email = %s", (User.email,))
        user_id = cur.fetchone()

        cur.execute("INSERT INTO cards (user_id, email) VALUES(%s,%s)",(user_id,User.email))
        mysql.connection.commit()
        cur.close()
        if cur.rowcount == 1:
            return 1
        else:
            return 0
    except Exception as e:
        print(f"Error: {e}")
        return 0

def userExist(User):
    cur = mysql.connection.cursor()
    try:
        cur.execute("SELECT * FROM users WHERE email = %s", (User.email,))
        result1 = cur.fetchone()
        cur.close()
        if result1:
            if check_password_hash(result1[3], User.password):
                return 1
            else:
                return 2
        else: 
            return 0   
    except Exception as e:
        print(f"Error: {e}")
        return 3

@auth.route("/login",methods=['GET','POST'])
def login_page():
    if request.method=="POST":
        session.pop("user", None)
        email = request.form['email']
        password = request.form['password']
        user = User(email, password,0,0)
        x = userExist(user)
        if x==1:
            session["user"] = user.email
            return redirect(url_for('views.home_page'))
        elif x==2:
            flash("Incorrect Password", category='error')
        elif x==0:
            flash("Invalid Credentials", category='error')
        else:
            flash("Authentication Error", category='error')
        
    return render_template('login.html', title="LOGIN", prompt="Create an account")

@auth.route("/signup",methods=['GET','POST'])
def signup_page():
    if request.method=="POST":
        session.pop("user", None)
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form["confirm password"]
        
        check = checkPassword(password, confirm_password)
        if check == 2:
            flash('Password must be atleast 7 characters', category='error')
        elif check==3:
            flash('Passwords do not match', category='error')
        elif check==4:
            flash('Password must contain a number', category='error')
        elif not("@" in email or "." in email):
            flash('Email must contain an @ symbol', category='error')
        else:
            user = User(email,password,0,0)
            x = uniqueEmail(user)
            if x:
                y = createUser(user)
                z = initializeCards(user)
                if y and z:
                    flash("Account created!", category='success')                    
                    return redirect(url_for('auth.login_page'))
                else:
                    flash("Registration failed. Please try again", category='error')
            else:
                flash("An account with that email already exist", category='error')
    return render_template('signup.html', title="REGISTER", prompt="Log in to an existing account")

@auth.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for('auth.login_page'))
