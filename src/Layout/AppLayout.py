from dash import Dash, html, dcc, ctx, callback, Output, Input, State
import dash_bootstrap_components as dbc
from Layout.AbstractLayout import AbstractLayout
from Layout.TitleLayout import TitleLayout
from Layout.MenuLayout import MenuLayout
from Layout.BaseGraphLayout import BaseGraphLayout

class AppLayout(AbstractLayout):
    
    def __init__(self, app: Dash):
        super(AppLayout, self).__init__()
        self.app = app
    
    def mainPage(self):
        self.children.append(TitleLayout())
        self.children.append(MenuLayout())
        self.children.append(BaseGraphLayout())
    
    def buildLayout(self):
        self.app.layout = html.Div([
            child.buildLayout() for child in self.children    
        ])
    
    def buildCallbacks(self):
        for child in self.children:
            child.buildCallbacks()
