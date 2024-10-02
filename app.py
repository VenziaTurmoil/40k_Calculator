from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd

import Graphs

app = Dash()

app.layout = html.Div(children=[
    html.H1(children='Simple Graph', style={'textAlign':'center'}),
    dcc.Graph(id='graph'),
    dcc.Slider(1, 12, 1, value=4, id='WA')
])

if __name__ == '__main__':
    app.run(debug=True)