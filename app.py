from website import create_app
from website import db

app = create_app()


if __name__ == "__main__":
    # with app.app_context():
    #     db.create_all()
    #     print('created schema')

    app.run(host='0.0.0.0',debug=True)
    print("Server is Running....")

