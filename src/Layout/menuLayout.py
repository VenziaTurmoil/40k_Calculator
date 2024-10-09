from dash import html, callback, Output, Input, State
import dash_bootstrap_components as dbc
from Layout.abstractLayout import AbstractLayout

class MenuLayout(AbstractLayout):
    
    def buildLayout(self):

        return html.Div([
            dbc.Button(
                "Open Menu",
                id="menu-btn",
                className="mb-3",
                color="primary",
                n_clicks=0,
            ),
            dbc.Collapse(
                dbc.Card([
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
    
    def buildCallbacks(self):
        
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