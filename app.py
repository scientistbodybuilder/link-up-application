from flask import Flask, render_template
from flask_mysqldb import MySQL
from dotenv import load_dotenv
import os
from flask_login import UserMixin

app = Flask(__name__)

app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


mysql = MySQL(app)

@app.route("/")
def home_page():
    return render_template('home.html')

@app.route("/contact")
def contact_page():
    return render_template('contact.html')

@app.route("/login")
def login_page():
    return render_template('login.html')

@app.route("/signup")
def signup_page():
    return render_template('signup.html')





if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)
    print("Server is Running....")

