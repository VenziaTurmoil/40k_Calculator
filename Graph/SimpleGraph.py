from dash import html, dcc, callback, Output, Input, State
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import copy
from Layout.AbstractLayout import AbstractLayout
from Model.Weapon import Weapon, options_list
from Model.Target import Target

class SimpleGraph(AbstractLayout):

    def __init__(self):
        super(AbstractLayout, self).__init__()
        self.id = 'simple-graph'
        self.weaponValues = {
            'A' :  { 'min':1, 'max':10, 'value':4, 'description':'Attacks'},
            'Sk' : { 'min':2, 'max':6,  'value':3, 'description':'Weapon Skill' },
            'S' :  { 'min':1, 'max':20, 'value':4, 'description':'Strength' },
            'AP' : { 'min':0, 'max':4,  'value':1, 'description':'Armor Penetration' },
            'D' :  { 'min':1, 'max':8,  'value':1, 'description':'Damage' },
        }
        self.targetValues = {
            'T' :  { 'min':1, 'max':12, 'value':5, 'description':'Toughness' },
            'Sv' : { 'min':2, 'max':7,  'value':4, 'description':'Save' },
            'Inv' : { 'min':2, 'max':7,  'value':6, 'description':'Invul' },
            'W' :  { 'min':1, 'max':12, 'value':3, 'description':'Wounds' },
        }
        self.graphValues = self.weaponValues | self.targetValues
        self.currentLine = {'axis': None, 'column': None, 'range': None}
        self.savedLines = []

    def buildLayout(self):

        return html.Div([
            dbc.Row([
                dbc.Col([
                    dcc.Graph(id='simple-graph-fig')
                ], id='simple-graph-graph-column-1', width=4),
                dbc.Col([
                    dcc.Graph(id='simple-graph-fig-compare')
                ], id='simple-graph-graph-column-2', width=4),
                dbc.Col([
                    dcc.Graph(id='simple-graph-fig-ratio')
                ], id='simple-graph-graph-column-3', width=4)
            ]),
            dbc.Row([
                dbc.Col([html.H3('Weapon Stats')] +
                        [html.Div([
                            html.P(weapon['description']),
                            dcc.Slider(
                                weapon['min'],
                                weapon['max'],
                                1,
                                value = weapon['value'],
                                id='simple-graph-input-{}'.format(key)
                            )
                        ]) for key, weapon in self.weaponValues.items()]
                ),
                dbc.Col([html.H3('Target Stats')] +
                        [html.Div([
                            html.P(target['description']),
                            dcc.Slider(
                                target['min'],
                                target['max'],
                                1,
                                value = target['value'],
                                id='simple-graph-input-{}'.format(key)
                            )
                        ]) for key, target in self.targetValues.items()] +
                        [dbc.Button("Save Graph", color="primary",
                                   id = 'simple-graph-btn-save'),
                        dbc.Button("Clear Graph", color="danger",
                                   id = 'simple-graph-btn-clear'),]
                ),
                dbc.Col([
                    html.H3('x-ordinate'),
                    dcc.RadioItems(
                        options=[
                                {'label': graphValues['description'], 'value': key}
                                for key, graphValues in self.graphValues.items()
                            ],
                        value='T',
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
            Output('simple-graph-fig-compare', 'figure'),
            Output('simple-graph-fig-ratio', 'figure'),
            [
                Input('simple-graph-input-{}'.format(key), 'value')
                for key in self.graphValues
            ] + [
                Input('simple-graph-input-radio', 'value'),
                Input('simple-graph-input-dropdown', 'value')
            ]
        )
        def draw_simple_graph(*inputs):
            radio = inputs[-2]
            options = inputs[-1]
            w = []
            t = []
            r = range(self.graphValues[radio]['min'], self.graphValues[radio]['max'] + 1)

            i = 0
            stats = {}
            for key in self.graphValues:
                stats[key] = inputs[i]
                i += 1

            for i in r:
                stats[radio] = i
                w.append(Weapon(stats['A'], stats['Sk'], stats['S'], stats['AP'], stats['D'], options))
                t.append(Target(stats['T'], stats['Sv'], stats['Inv'], stats['W'], 0))

            self.currentLine['axis'] = self.graphValues[radio]['description']
            self.currentLine['column'] = np.array([w[i].sequence(t[i]) for i in range(len(w))])
            self.currentLine['range'] = r

            df_graph = pd.DataFrame()
            df_graph[self.currentLine['axis']] = self.currentLine['range']
            df_graph[0] = self.currentLine['column']
            i = 0
            for line in self.savedLines:
                if line['axis'] == self.currentLine['axis'] and line['range'] == self.currentLine['range']:
                    i += 1
                    df_graph[i] = line['column']

            graph = px.line(df_graph,
                            x=self.currentLine['axis'],
                            y=df_graph.columns,
                            markers=True,
            )
            graph.update_yaxes(title='AVG Damage', range=[0, None])

            compare = {}
            if len(self.savedLines) >= 1:
                df_compare = pd.DataFrame()
                df_compare[self.currentLine['axis']] = self.currentLine['range']
                for line in self.savedLines:
                    if line['axis'] == self.currentLine['axis'] and line['range'] == self.currentLine['range']:
                        i += 1
                        df_compare[i] = self.currentLine['column'] - line['column']

                only_data = df_compare.drop(self.currentLine['axis'], axis=1)

                compare = px.line(df_compare, x=self.currentLine['axis'], y=df_compare.columns, markers=True)
                compare.update_yaxes(title='AVG Damage Difference',
                                        range = [min(-0.1, only_data.min().min()-0.1),
                                                max(0.1, only_data.max().max()+0.1)],
                                        zeroline=True,
                                        zerolinewidth=2,
                                        zerolinecolor='black')

            ratio = {}
            if len(self.savedLines) >= 1:
                df_ratio = pd.DataFrame()
                df_ratio[self.currentLine['axis']] = self.currentLine['range']
                for line in self.savedLines:
                    if line['axis'] == self.currentLine['axis'] and line['range'] == self.currentLine['range']:
                        i += 1
                        df_ratio[i] = self.currentLine['column'] / line['column']

                only_data = df_ratio.drop(self.currentLine['axis'], axis=1)

                ratio = px.line(df_ratio, x=self.currentLine['axis'], y=df_ratio.columns, markers=True)
                ratio.update_yaxes(title='AVG Damage Ratio',
                                    range=[only_data.min().min()-0.1, only_data.max().max()+0.1])
                ratio.add_trace(go.Scatter(
                    x=[i for i in self.currentLine['range']],
                    y=[1 for _ in self.currentLine['range']],
                    name='origin',
                    mode='lines',
                    line=dict(
                        width=2,
                        color='black'
                    )
                ))

            return graph, compare, ratio

        @callback(
            [
                Output('simple-graph-input-{}'.format(key), 'disabled')
                for key in self.graphValues
            ],
            Input('simple-graph-input-radio', 'value'),
        )
        def disable_sliders(value):
            #absolument immonde
            res = [False for key in self.graphValues]
            k = 0
            for key in self.graphValues:
                if key == value:
                    res[k] = True
                k += 1
            return res

        @callback(
            Input('simple-graph-btn-save', 'n_clicks')
        )
        def save_line(n):
            if n and len(self.savedLines) <= 6:
                self.savedLines.append(copy.deepcopy(self.currentLine))

        @callback(
            Input('simple-graph-btn-clear', 'n_clicks')
        )
        def clear_save(n):
            if n:
                self.savedLines.clear()