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
    dbc.Row([
        dbc.Col([
            html.H3('Weapon Stats'),
            html.P('Attacks'),
            dcc.Slider(1, 9, 1,
                       value=3,
                       id='graph-basic-input-A'),
            html.P('Weapon Skill'),
            dcc.Slider(2, 6, 1,
                       value=3,
                       id='graph-basic-input-Sk'),
            html.P('Strength'),
            dcc.Slider(1, 14, 1,
                       value=4,
                       id='graph-basic-input-S'),
            html.P('Armor Penetration'),
            dcc.Slider(0, 4, 1,
                       value=1,
                       id='graph-basic-input-AP'),
            html.P('Damage'),
            dcc.Slider(1, 8, 1,
                       value=1,
                       id='graph-basic-input-D')
        ]),
        dbc.Col([
            html.H3('Target Stats'),
            html.P('Toughness'),
            dcc.Slider(1, 12, 1,
                       value=5,
                       id='graph-basic-input-T'),
            html.P('Save'),
            dcc.Slider(1, 7, 1,
                       value=4,
                       id='graph-basic-input-Sv'),
            html.P('Wounds'),
            dcc.Slider(1, 12, 1,
                       value=3,
                       id='graph-basic-input-W')
        ]),
        dbc.Col([
            html.H3('Column to Freeze'),
            dcc.RadioItems(
                options=[
                    {'label': 'Attacks', 'value': '0'},
                    {'label': 'Weapon Skill', 'value': '1'},    
                    {'label': 'Strength', 'value': '2'},    
                    {'label': 'Armor Penetration', 'value': '3'},    
                    {'label': 'Damage', 'value': '4'},    
                    {'label': 'Toughness', 'value': '5'},    
                    {'label': 'Save', 'value': '6'},    
                    {'label': 'Wounds', 'value': '7'} 
                ], 
                value='5',
                id='graph-basic-input-radio'
            )
        ])
    ])
], id='graph-basic-collapse')

@callback(
    Output("graph-basic-collapse", "is_open"),
    Input("graph-basic-btn", "n_clicks"),
)
def open_graph_basic(n):
    if n:
        return True
    return False
