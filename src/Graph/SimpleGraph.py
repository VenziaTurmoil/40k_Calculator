from dash import html, dcc, callback, Output, Input, State
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from Layout.AbstractLayout import AbstractLayout
from Model.Weapon import Weapon, options_list
from Model.Target import Target

class SimpleGraph(AbstractLayout):
    
    def __init__(self):
        super(AbstractLayout, self).__init__()
        self.id = 'simple-graph'
        
    def buildLayout(self):

        return html.Div([
            dcc.Graph(id='simple-graph-fig'),
            dbc.Row([
                dbc.Col([
                    html.H3('Weapon Stats'),
                    html.P('Attacks'),
                    dcc.Slider(1, 9, 1,
                                value=3,
                                id='simple-graph-input-A'),
                    html.P('Weapon Skill'),
                    dcc.Slider(2, 6, 1,
                                value=3,
                                id='simple-graph-input-Sk'),
                    html.P('Strength'),
                    dcc.Slider(1, 14, 1,
                                value=4,
                                id='simple-graph-input-S'),
                    html.P('Armor Penetration'),
                    dcc.Slider(0, 4, 1,
                                value=1,
                                id='simple-graph-input-AP'),
                    html.P('Damage'),
                    dcc.Slider(1, 8, 1,
                                value=1,
                                id='simple-graph-input-D')
                ]),
                dbc.Col([
                    html.H3('Target Stats'),
                    html.P('Toughness'),
                    dcc.Slider(1, 12, 1,
                                value=5,
                                id='simple-graph-input-T'),
                    html.P('Save'),
                    dcc.Slider(1, 7, 1,
                                value=4,
                                id='simple-graph-input-Sv'),
                    html.P('Wounds'),
                    dcc.Slider(1, 12, 1,
                                value=3,
                                id='simple-graph-input-W')
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
                        id='simple-graph-input-radio'
                    ),
                    html.H3('Additionnal options'),
                    dcc.Dropdown(
                        options_list,
                        [],
                        multi=True,
                        id='simple-graph-input-dropdown'
                    )
                ])
            ])
        ], id='simple-graph-div', style={'display': 'none'})
    
    def buildCallbacks(self):
        
        @callback(
            Output('simple-graph-fig', 'figure'),
            Input('simple-graph-input-A', 'value'),
            Input('simple-graph-input-Sk', 'value'),
            Input('simple-graph-input-S', 'value'),
            Input('simple-graph-input-AP', 'value'),
            Input('simple-graph-input-D', 'value'),
            Input('simple-graph-input-T', 'value'),
            Input('simple-graph-input-Sv', 'value'),
            Input('simple-graph-input-W', 'value'),
            Input('simple-graph-input-radio', 'value'),
            Input('simple-graph-input-dropdown', 'value')
        )
        def draw_simple_graph(A, Sk, S, AP, D, T, Sv, W, radio, options):
            r = int(radio)
            names = ['Attacks', 'Weapon Skill', 'Strength', 'Armor Penetration',
                     'Damage', 'Toughness', 'Save', 'Wounds']
            stats = [A, Sk, S, AP, D, T, Sv, W]
            ranges = [range(1, 10), range(2, 7), range(1, 15), range(0, 5),
                      range(1, 9), range(1, 13), range(1, 8), range(1, 7)]
        
            w = []
            t = []
            for i in ranges[r]:
                stats[r] = i
                w.append(Weapon(stats[0], stats[1], stats[2], stats[3], stats[4], options))
                t.append(Target(stats[5], stats[6], stats[7], 0))
            
            df = pd.DataFrame()
            df[names[r]] = ranges[r]
            df['AVG Damage'] = [w[i].sequence(t[i]) for i in range(len(w))]
                
            return px.line(df, x=names[r], y='AVG Damage', markers=True)