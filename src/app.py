from dash import Dash, html, dcc, ctx, callback, Output, Input, State
import plotly.express as px
import dash_bootstrap_components as dbc

from Layout.appLayout import AppLayout

external_stylesheets = [dbc.themes.BOOTSTRAP]
app = Dash(__name__, external_stylesheets=external_stylesheets)

layout = AppLayout(app)

layout.mainPage()

layout.buildLayout()
layout.buildCallbacks()

if __name__ == '__main__':
    app.run(debug=True)