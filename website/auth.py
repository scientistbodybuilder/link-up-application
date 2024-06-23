from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from .model import mysql
from functools import wraps

auth=Blueprint('auth', __name__)

class User:
    def __init__(self,email,password):
        self.email = email
        self.password = password

def contains_num(s):
    for char in s:
        if char.isdigit():
            return True
    return False

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

@auth.route("/",methods=['GET','POST'])
def login_page():
    if request.method=="POST":
        session.pop("user", None)
        email = request.form['email']
        password = request.form['password']
        user = User(email, password)
        x = userExist(user)
        if x==1:
            flash("Authetication Succesful", category='success')
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
        
        if len(password)<7:
            flash('Password must be atleast 7 characters', category='error')
        elif not contains_num(password):
            flash('Password must contain a number', category='error')
        elif not("@" in email):
            flash('Email must contain an @ symbol', category='error')
        else:
            user = User(email,password)
            x = uniqueEmail(user)
            if x:
                y = createUser(user)
                if y:
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
