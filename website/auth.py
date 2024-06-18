from flask import Blueprint, render_template, request, flash, redirect
from werkzeug.security import generate_password_hash, check_password_hash


auth=Blueprint('auth', __name__)

def contains_num(s):
    for char in s:
        if char.isdigit():
            return True
    return False

@auth.route("/login",methods=['GET','POST'])
def login_page():
    if request.method=="POST":
        from app import mysql
        email = request.form['email']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s AND passwrd = %s",(email,password))
        cur.commit()
        if cur.rowcount ==1:
            flash('Authentication succesful', category='success')
        else:
            flash('Authentication failed', category='error')
        
        cur.close()
        
    return render_template('login.html')

@auth.route("/signup",methods=['GET','POST'])
def signup_page():
    if request.method=="POST":
        from app import mysql
        email = request.form['email']
        password = request.form['password']
        
        if len(password)<7:
            flash('Password must be atleast 7 characters', category='error')
        elif not contains_num(password):
            flash('Password must contain a number', category='error')
        elif not("@" in email):
            flash('Email must contain an @ symbol', category='error')
        elif not(".com" in email):
            flash("Email contain '.com'", category='error')
        else:
            cur = mysql.connection.cursor()
            cur.execute("INERT INTO users (email,passwrd) VALUES (%s,%s)",(email,password))
            mysql.connection.commit()
            if cur.rowcount == 1:
                flash("Account created!", category='success')                    
                return redirect('login.html')
            else:
                flash("Registration failed. Please try again", category='error')
            
            cur.close()

    return render_template('signup.html')