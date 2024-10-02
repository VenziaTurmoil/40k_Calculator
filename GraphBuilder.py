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
    df = pd.DataFrame()
    match radio:
        case 'A':
            w = [Weapon(i, Sk, S, AP, D) for i in range(1, 10)]
            t = Target(T, Sv, W, 0)
            df['Attacks'] = range(1, 10)
            df['AVG Damage'] = [i.sequence(t) for i in w]
            return px.line(df, x='Attacks', y='AVG Damage', markers=True)
        case 'Sk':
            w = [Weapon(A, i, S, AP, D) for i in range(2, 7)]
            t = Target(T, Sv, W, 0)
            df['Weapon Skill'] = range(2, 7)
            df['AVG Damage'] = [i.sequence(t) for i in w]
            return px.line(df, x='Weapon Skill', y='AVG Damage', markers=True)
        case 'S':
            w = [Weapon(A, Sk, i, AP, D) for i in range(1, 15)]
            t = Target(T, Sv, W, 0)
            df['Strength'] = range(1, 15)
            df['AVG Damage'] = [i.sequence(t) for i in w]
            return px.line(df, x='Strength', y='AVG Damage', markers=True)
        case 'AP':
            w = [Weapon(A, Sk, S, i, D) for i in range(0, 5)]
            t = Target(T, Sv, W, 0)
            df['Armor Penetration'] = range(0, 5)
            df['AVG Damage'] = [i.sequence(t) for i in w]
            return px.line(df, x='Armor Penetration', y='AVG Damage', markers=True)
        case 'D':
            w = [Weapon(A, Sk, S, Sv, i) for i in range(1, 9)]
            t = Target(T, Sv, W, 0)
            df['Damage'] = range(1, 9)
            df['AVG Damage'] = [i.sequence(t) for i in w]
            return px.line(df, x='Damage', y='AVG Damage', markers=True)
        case 'T':
            w = Weapon(A, Sk, S, AP, D)
            t = [Target(i, Sv, W, 0) for i in range(1, 13)]
            df['Toughness'] = range(1, 13)
            df['AVG Damage'] = [w.sequence(i) for i in t]
            return px.line(df, x='Toughness', y='AVG Damage', markers=True)
        case 'Sv':
            w = Weapon(A, Sk, S, AP, D)
            t = [Target(T, i, W, 0) for i in range(1, 8)]
            df['Save'] = range(1, 8)
            df['AVG Damage'] = [w.sequence(i) for i in t]
            return px.line(df, x='Save', y='AVG Damage', markers=True)
        case 'W':
            w = Weapon(A, Sk, S, AP, D)
            t = [Target(T, Sv, i, 0) for i in range(1, 7)]
            df['Wounds'] = range(1, 7)
            df['AVG Damage'] = [w.sequence(i) for i in t]
            return px.line(df, x='Wounds', y='AVG Damage', markers=True)
        case 'Sv':
            w = Weapon(A, Sk, S, AP, D)
            t = [Target(T, i, W, 0) for i in range(1, 7)]
            df['Toughness'] = range(1, 13)
            df['AVG Damage'] = [w.sequence(i) for i in t]
            return px.line(df, x='Toughness', y='AVG Damage', markers=True)
        case _:
            raise ValueError("Bad value in radio button")