from dash import html, dcc
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.express as px
from assets.py_style import *

### Layout ###
clustering_layout = html.Div([
    dbc.Card(
        dbc.CardBody([
            html.Div(html.P("✨ Coming soon: clustering analysis of exoplanets! ✨"),)],
                   style=card_body_style,
        ),
    style=card_style),
], style=overview_layout_style)