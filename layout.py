from dash import Dash, html, dcc, ctx, callback, Output, Input, State
import plotly.express as px
import dash_bootstrap_components as dbc

title = html.Div(html.H1('40k_Calculator'),
        className='d-flex justify-content-center')

menu = html.Div([
    dbc.Button(
        "Open Menu",
        id="menu-btn",
        className="mb-3",
        color="primary",
        n_clicks=0,
    ),
    dbc.Collapse(
        dbc.Card([
            dbc.CardImg(src="/assets/placeholder286x180.png", top=True),
            dbc.CardBody([
                html.H4("Basic Graph", className="card-title"),
                html.P(
                    "Basic Graph with Manual configuration",
                    className="card-text",
                ),
                dbc.Button("Go to Basic Graph", color="primary",
                           id = 'graph-basic-btn'),
            ]),
        ], style={'width': '18rem'}),
        id="menu-collapse",
        is_open=False,
    ),
])

@callback(
    Output("menu-collapse", "is_open"),
    Output("menu-btn", "children"),
    Input("menu-btn", "n_clicks"),
    State("menu-collapse", "is_open"),
)
def toggle_menu_collapse(n, is_open):
    if n:
        return not is_open, "Open Menu" if is_open else "Close Menu"
    return is_open, "Open Menu"

graph_basic = dbc.Collapse([
    dcc.Graph(id='graph-basic-fig'),
    dcc.Slider(1, 12, 1,
        value=4,
        id='graph-basic-input-WA'
    )
], id='graph-basic-collapse')

@callback(
    Output("graph-basic-collapse", "is_open"),
    Input("graph-basic-btn", "n_clicks"),
)
def open_graph_basic(n):
    if n:
        return True
    return False
