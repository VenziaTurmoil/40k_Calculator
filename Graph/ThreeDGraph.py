from dash import html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import copy
from Layout.AbstractLayout import AbstractLayout
from Model.Weapon import Weapon, options_list
from Model.Target import Target

class ThreeDGraph(AbstractLayout):

    def __init__(self):
        super(AbstractLayout, self).__init__()
        self.id = '3d-graph'
        self.weaponValues = {
            'A' :  { 'min':1, 'max':10, 'value':5, 'description':'Attacks'},
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
        self.currentSurface = {'axis': None, 'data': None, 'range': None}
        self.savedSurfaces = []

    def buildLayout(self):

        return html.Div([
            dcc.Graph(id='3d-graph-fig'),
            dbc.Row([
                dbc.Col([html.H3('Weapon Stats')] +
                        [html.Div([
                            html.P(weapon['description']),
                            dcc.Slider(
                                weapon['min'],
                                weapon['max'],
                                1,
                                value = weapon['value'],
                                id='3d-graph-input-{}'.format(key)
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
                                id='3d-graph-input-{}'.format(key)
                            )
                        ]) for key, target in self.targetValues.items()] +
                        [dbc.Button("Save Graph", color="primary",
                                   id = '3d-graph-btn-save'),
                        dbc.Button("Clear Graph", color="danger",
                                   id = '3d-graph-btn-clear'),]
                ),
                dbc.Col([
                    html.H3('x-ordinate'),
                    dcc.Checklist(
                        options=[
                                {'label': graphValues['description'], 'value': key}
                                for key, graphValues in self.graphValues.items()
                            ],
                        value=['T', 'Sv'],
                        id = '3d-graph-input-naive-checklist'
                    ),
                    dcc.Checklist(
                        options=[
                                {'label': graphValues['description'], 'value': key}
                                for key, graphValues in self.graphValues.items()
                            ],
                        value=['T', 'Sv'],
                        id = '3d-graph-input-true-checklist',
                        style = {'display' : 'none'}
                    ),
                    html.P('2 and only 2 boxes must be checked',
                           id = '3d-graph-label-checklist',
                           style = {'display' : 'none'}
                    ),
                    html.H3('Additionnal options'),
                    dcc.Dropdown(
                        options_list,
                        [],
                        multi=True,
                        id='3d-graph-input-dropdown'
                    )
                ])
            ])
        ], id='3d-graph-div', style={'display': 'none'})

    def buildCallbacks(self):

        @callback(
            Output('3d-graph-input-true-checklist', 'value'),
            Output('3d-graph-label-checklist', 'style'),
            Input('3d-graph-input-naive-checklist', 'value'),
            Input('3d-graph-input-true-checklist', 'value'),
        )
        def verify_checklist(naive, true):
            if len(naive) == 2:
                return naive, {'display' : 'none'}
            else:
                return true, {'display' : 'grid'}

        @callback(
            Output('3d-graph-fig', 'figure'),
            [
                Input('3d-graph-input-{}'.format(key), 'value')
                for key in self.graphValues
            ] + [
                Input('3d-graph-input-true-checklist', 'value'),
                Input('3d-graph-input-dropdown', 'value')
            ]
        )
        def draw_3d_graph(*inputs):
            checklist = inputs[-2]
            options = inputs[-1]
            w = []
            t = []
            r = [
                    range(self.graphValues[checklist[0]]['min'], self.graphValues[checklist[0]]['max'] + 1),
                    range(self.graphValues[checklist[1]]['min'], self.graphValues[checklist[1]]['max'] + 1),
            ]

            i = 0
            stats = {}
            for key in self.graphValues:
                stats[key] = inputs[i]
                i += 1

            k = -1
            for i in r[0]:
                k += 1
                w.append([])
                t.append([])
                for j in r[1]:
                    stats[checklist[0]] = i
                    stats[checklist[1]] = j
                    w[k].append(Weapon(stats['A'], stats['Sk'], stats['S'], stats['AP'], stats['D'], options))
                    t[k].append(Target(stats['T'], stats['Sv'], stats['W'], 0))

            self.currentSurface['axis'] = {
                'x' : self.graphValues[checklist[0]]['description'],
                'y' : self.graphValues[checklist[1]]['description'],
            }
            self.currentSurface['data'] = [[w[i][j].sequence(t[i][j]) for j in range(len(w[i]))] for i in range(len(w))]
            self.currentSurface['range'] = r

            active_surfaces = []
            for surface in self.savedSurfaces:
                if self.currentSurface['axis'] == surface['axis']:
                    active_surfaces.append(surface)

            fig = go.Figure(data = [
                go.Surface(z=surface['data'], showscale=False, opacity=0.75) for surface in active_surfaces
            ] + [go.Surface(z=self.currentSurface['data'], opacity=0.8)])

            fig.update_layout(
                scene = dict(
                    xaxis_title = self.currentSurface['axis']['x'],
                    yaxis_title = self.currentSurface['axis']['y'],
                    zaxis_title = 'AVG Damage',
                    zaxis = dict(range=[0, None])
                )
            )

            return fig

        @callback(
            Input('3d-graph-btn-save', 'n_clicks')
        )
        def save_line(n):
            if n:
                self.savedSurfaces.append(copy.deepcopy(self.currentSurface))

        @callback(
            Input('3d-graph-btn-clear', 'n_clicks')
        )
        def clear_save(n):
            if n:
                self.savedSurfaces.clear()