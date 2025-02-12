from website import create_app
from website import db
import pandas as pd
# from dash import Dash
# from website.analytic import data
from flask import session
from website.model import Users


app = create_app()

if __name__ == "__main__":
#     with app.app_context():
#         db.create_all()
#         print('created schema')
    #app layout
    

    #     dash_app = Dash(
    #         __name__,
    #         server=app,
    #         url_base_pathname='/dashboard/'
    #     )
    #     if not data.empty:
    #         list_options = list(set(data['Location'].to_list()))
    #         dash_app.layout = create_layout(dash_app,list_options,data)
    #     else:
    #         dash_app.layout = create_layout()

    app.run(host='0.0.0.0',debug=True)
    print("Server is Running....")

