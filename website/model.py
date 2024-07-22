from flask_mysqldb import MySQL
from flask_mail import Mail

mysql = MySQL()
mail = Mail()

def init_db(app):
    mysql.init_app(app)
    return mysql

def init_mail(app):
    mail.init_app(app)
    return mail