# from dash import Dash, html, dcc
# from dash.dependencies import Input, Output
# from . import ids
# def render(app,location_options):

#     @app.callback(
#         Output(ids.LOCATION_DROPDOWN, "value"),
#         Input(ids.LOCATION_DROPDOWN_SELECT_ALL, "n_clicks"),
#     )
#     def select_all_locations(_: int) -> list[str]:
#         return location_options
#     return html.Div(
#         children=[
#             dcc.Dropdown(
#                 options=[{"label":location,"value":location} for location in location_options],
#                 multi=True,
#                 value=location_options,
#                 id=ids.LOCATION_DROPDOWN
#             ),
#             html.Button(
#                 className='select-all-button',
#                 children=['Select All'],
#                 id=ids.LOCATION_DROPDOWN_SELECT_ALL
#             )
#         ]
#     )