from Weapon import Weapon
from Target import Target

import plotly.express as px
from dash import Dash, dcc, html, callback, Input, Output
import json
import pandas as pd

@callback(
    Output('graph', 'figure'),
    Input('WA', 'value')
)
def simpleGraph(value):
    w = Weapon(1, 3, value, 0, 1)
    a_t = [Target(i, 3, 2, 1) for i in range(1, 13)]
    
    df = pd.DataFrame()
    
    df['Toughness'] = range(1, 13)
    df['AVG Damage'] = [w.sequence(t) for t in a_t]
    
    fig = px.line(df, x="Toughness", y="AVG Damage")
    return fig
