from dash import Dash, html, dcc, ctx, callback, Output, Input, State
import plotly.express as px
import dash_bootstrap_components as dbc
import os

from Layout.AppLayout import AppLayout

external_stylesheets = [dbc.themes.BOOTSTRAP]
app = Dash(__name__, external_stylesheets=external_stylesheets)

layout = AppLayout(app)

layout.mainPage()

layout.buildLayout()
layout.buildCallbacks()

if __name__ == '__main__':
    if os.environ.get('CONTAINER', False):
        app.run(debug=False, host='0.0.0.0', port='8000')
    else:
        app.run(debug=True, host='127.0.0.1', port='8050')
