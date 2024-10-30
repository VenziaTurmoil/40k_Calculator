from dash import html, callback, Output, Input, State, ctx
import dash_bootstrap_components as dbc
from Layout.AbstractLayout import AbstractLayout
from Graph.SimpleGraph import SimpleGraph
from Graph.ThreeDGraph import ThreeDGraph

class BaseGraphLayout(AbstractLayout):

    def __init__(self):
        super(AbstractLayout, self).__init__()
        self.children = [SimpleGraph(), ThreeDGraph()]

    def buildLayout(self):

        return html.Div([
            html.Div([
                child.buildLayout() for child in self.children
            ]),
            html.Div('empty', id='base-graph-active', style={'display': 'none'})
        ], id='base-graph-div')

    def buildCallbacks(self):

        for child in self.children:
            child.buildCallbacks()

        @callback(
            [Output("base-graph-active", "children")] +
            [Output("{}-div".format(graph_div.id), "style") for graph_div in self.children],
            [Input("menu-{}-btn".format(graph_div.id), "n_clicks") for graph_div in self.children],
            prevent_initial_call=True
        )
        def activate_graph(*ns):
            return [ctx.triggered_id] + [
                    {'display': 'grid'} if "menu-{}-btn".format(graph_div.id) == ctx.triggered_id else {'display': 'none'}
                    for graph_div in self.children
                ] if ns else ['empty'] + [{'display': 'none'} for graph_div in self.children]