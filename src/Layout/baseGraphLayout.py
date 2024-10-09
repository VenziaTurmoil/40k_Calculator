from dash import html, callback, Output, Input, State
import dash_bootstrap_components as dbc
from Layout.abstractLayout import AbstractLayout

class BaseGraphLayout(AbstractLayout):
    
    def buildLayout(self):

        return html.Div([
            child.buildLayout() for child in self.children
        ], id='base-graph-div')
    
    def buildCallbacks(self):
        
        for child in self.children:
            child.buildCallbacks()