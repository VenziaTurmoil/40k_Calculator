from Weapon import Weapon
from Target import Target

import plotly.express as px
from dash import Dash, dcc, html, callback, Input, Output
import json
import pandas as pd

@callback(
    Output('graph-basic-fig', 'figure'),
    Input('graph-basic-input-A', 'value'),
    Input('graph-basic-input-Sk', 'value'),
    Input('graph-basic-input-S', 'value'),
    Input('graph-basic-input-AP', 'value'),
    Input('graph-basic-input-D', 'value'),
    Input('graph-basic-input-T', 'value'),
    Input('graph-basic-input-Sv', 'value'),
    Input('graph-basic-input-W', 'value'),
    Input('graph-basic-input-radio', 'value')
)
def simpleGraph(A, Sk, S, AP, D, T, Sv, W, radio):
    r = int(radio)
    names = ['Attacks', 'Weapon Skill', 'Strength', 'Armor Penetration',
             'Damage', 'Toughness', 'Save', 'Wounds']
    stats = [A, Sk, S, AP, D, T, Sv, W]
    ranges = [range(1, 10), range(2, 7), range(1, 15), range(0, 5),
              range(1, 9), range(1, 13), range(1, 8), range(1, 7)]

    w = []
    t = []
    for i in ranges[r]:
        stats[r] = i
        w.append(Weapon(stats[0], stats[1], stats[2], stats[3], stats[4]))
        t.append(Target(stats[5], stats[6], stats[7], 0))
    
    df = pd.DataFrame()
    df[names[r]] = ranges[r]
    df['AVG Damage'] = [w[i].sequence(t[i]) for i in range(len(w))]
        
    return px.line(df, x=names[r], y='AVG Damage', markers=True)