import pandas as pd
from .model import Users, Cards, db
from flask import session
from dash import Dash, dcc, html

#get the account email
def init_dashboard(server):
    dash_app = Dash(
        __name__,
        server=server,
        url_base_pathname='/dashboard/'
    )

    return dash_app


