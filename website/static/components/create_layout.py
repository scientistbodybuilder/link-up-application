# from dash import Dash, html
# from website.static.components import location_dropdown
# from website.static.components import line_chart

# def create_layout(dashapp,list_options,data,org):
#     if org:
#         return html.Div(
#             className="dashapp-div",
#             children=[
#                 html.Div(
#                     className='dropdown-container',
#                     children=[
#                         location_dropdown.render(dashapp,list_options)
#                     ]
#                 ),
#                 line_chart.render(dashapp,data)
#             ]
#         )
#     else:
#         return html.Div(
#             html.H2("You are not an organizations with a review page"),
#             html.H6("Problem? Contact us at linkup")
#         )