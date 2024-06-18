from flask import Blueprint, render_template
#from app import mysql

views=Blueprint('views', __name__)

@views.route('/')
def home_page():
    return render_template('home.html')

@views.route("/contact")
def contact_page():
    return render_template('contact.html')


