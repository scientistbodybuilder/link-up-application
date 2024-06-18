from website import create_app
from flask_mysqldb import MySQL

app = create_app()
mysql = MySQL(app)

if __name__ == "__main__":
    app.run(host='0.0.0.0',debug=True)
    print("Server is Running....")

