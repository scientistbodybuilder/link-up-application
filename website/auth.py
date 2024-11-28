from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from .model import mysql
from functools import wraps
import smtplib, os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Template
from dotenv import load_dotenv

auth=Blueprint('auth', __name__)
load_dotenv()
HOST = "smtp.gmail.com"
PORT = 587
FROM_EMAIL = "linkup.tech.canada@gmail.com"
PASSWORD = os.getenv('LINKUP_EMAIL_PASSWORD')
TO_EMAIL = ""

class User:
    def __init__(self,email,password,linktree_card, direct_card):
        self.email = email
        self.password = password
        self.LT_card = linktree_card
        self.D_card = direct_card
        self.user_id=""
        self.org_name = ""


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


def uniqueEmail(email):
    cur = mysql.connection.cursor()
    try:
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
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
    
def uniqueOrganization(org_name):
    cur = mysql.connection.cursor()
    try:
        cur.execute("SELECT * FROM users WHERE org_name = %s", (org_name))
        org = cur.fetchone()
        if org:
            print("Existing organization")
            return False
        else:
            return True
    except Exception as e:
            print(f"Error in uniqueOrganization: {e}")
            return False

def createUser(User):
    cur = mysql.connection.cursor()
    hashed_password = generate_password_hash(User.password, method='pbkdf2:sha256')
    try:
        cur.execute("INSERT INTO users (org_name,email,passwrd) VALUES (%s,%s,%s)", (User.org_name,User.email,hashed_password))
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

        cur.execute("INSERT INTO cards (user_id, org_name, email) VALUES(%s,%s,%s)",(user_id,User.org_name,User.email))
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
                obj = {
                    'exist':1,
                    'id': result1[0]
                }
                return obj
            else:
                return {'exist':2}
        else: 
            return {'exist':0}   
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
        if x['exist']==1:
            session["user"] = user.email
            session["id"] = x['id']
            return redirect(url_for('views.home_page'))
        elif x['exist']==2:
            flash("Incorrect Password", category='error')
        elif x['exist']==0:
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
        org_name = request.form["org_name"]
        
        check = checkPassword(password, confirm_password)
        if check == 2:
            flash('Password must be atleast 7 characters', category='error')
        elif check==3:
            flash('Passwords do not match', category='error')
        elif check==4:
            flash('Password must contain a number', category='error')
        elif not("@" in email or "." in email):
            flash('Email must contain an @ symbol', category='error')
        elif (org_name != "") and (not(uniqueOrganization(org_name))):
            flash('The organization name already exists', category='error')
        else:
            user = User(email,password,0,0)
            user.org_name = org_name
            x = uniqueEmail(user.email)
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

@auth.route("/recovery", methods=['GET','POST'])
def recovery_page():
    session.pop("user", None)
    if request.method == "POST":
        TO_EMAIL = request.form['email']
        #verify whether the email is valid
        valid = uniqueEmail(TO_EMAIL)
        if not valid:
            message = MIMEMultipart()
            message["From"] = FROM_EMAIL
            message["To"] = TO_EMAIL
            message["Subject"] = "LinkUp This is your Recovery URL"
            html_content = """
            <html>
            <body>
                <p>This is your recovery URL: {{ URL }}</p>
                <br>
                <p>LinkUp Canda</p>
                <p>linkup.tech.canada@gmail.com</p>                      
                <br>
            </body>
            </html>
            """
            template = Template(html_content)
            html = template.render(URL = "some URL")
            try:
                server = smtplib.SMTP(HOST,PORT)
                server.starttls()
                message.attach(MIMEText(html, 'html'))
                server.login(FROM_EMAIL,PASSWORD)
                server.sendmail(FROM_EMAIL,TO_EMAIL,message.as_string())
                server.quit()
                flash("Email sent successfully",category='success')
            except Exception as e:
                print(f"Sending Recovery Email: {e}")
                flash("Error in sending email. Try again",category='error')
        else:
            flash("Email not in the system",category='error')
    return render_template('recovery.html')
