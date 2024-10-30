from dash import html, dcc, callback, Output, Input, State
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
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
            'Sv' : { 'min':1, 'max':7,  'value':4, 'description':'Save' },
            'W' :  { 'min':1, 'max':12, 'value':3, 'description':'Wounds' },
        }
        self.graphValues = self.weaponValues | self.targetValues
        self.currentLine = {'axis': None, 'column': None, 'range': None}
        self.savedLines = []

    def buildLayout(self):

        return html.Div([
            dcc.Graph(id='simple-graph-fig'),
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
                t.append(Target(stats['T'], stats['Sv'], stats['W'], 0))

            self.currentLine['axis'] = self.graphValues[radio]['description']
            self.currentLine['column'] = [w[i].sequence(t[i]) for i in range(len(w))]
            self.currentLine['range'] = r

            df = pd.DataFrame()
            df[self.currentLine['axis']] = self.currentLine['range']
            df[0] = self.currentLine['column']
            i = 0
            for line in self.savedLines:
                if line['axis'] == self.currentLine['axis'] and line['range'] == self.currentLine['range']:
                    i += 1
                    df[i] = line['column']

            fig = px.line(df, x=self.currentLine['axis'], y=df.columns, markers=True)
            fig.update_yaxes(title='AVG Damage', range=[0, None])

            return fig

        @callback(
            Input('simple-graph-btn-save', 'n_clicks')
        )
        def save_line(n):
            if n:
                self.savedLines.append(copy.deepcopy(self.currentLine))

        @callback(
            Input('simple-graph-btn-clear', 'n_clicks')
        )
        def clear_save(n):
            if n:
                self.savedLines.clear()