from dash import html, dcc, callback, Output, Input, State
import dash_bootstrap_components as dbc
import os
from Layout.abstractLayout import AbstractLayout

class MenuLayout(AbstractLayout):
    
    def buildLayout(self):

        return dbc.Collapse([
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
    
    def buildCallbacks(self):
        
        @callback(
            Output("base-graph-div", "style"),
            Output("graph-basic-div", "style"),
            Input("graph-basic-btn", "n_clicks"),
        )
        def open_graph_basic(n):
            if n:
                return True
            return False


