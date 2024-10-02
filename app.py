from dash import Dash, html, dcc, ctx, callback, Output, Input, State
import plotly.express as px
import dash_bootstrap_components as dbc

import GraphBuilder
import layout as lt

external_stylesheets = [dbc.themes.DARKLY]
app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    lt.title,
    lt.menu,
    lt.graph_basic
])




if __name__ == '__main__':
    app.run(debug=True)