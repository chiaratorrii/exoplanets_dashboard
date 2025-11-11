from dash import html, dcc
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.express as px
from assets.py_style import *


# Load data
exoplanets = pd.read_csv("data\exoplanets_data.csv") 
unique_exo = exoplanets.sort_values(['pl_name', 'releasedate'], ascending=[True, False]).drop_duplicates(subset='pl_name', keep='first')


### Components ###

# Total number of exoplanets discovered section
tot_num_exoplanets = html.Div(children=[
    html.Div(id="total-exoplanets", children=[html.H1(len(unique_exo.pl_name.unique()))], style=tot_num_style),
    html.P("exoplanets discovered", style=tot_num_text_style_1),
    html.Div(id="last_update", children=[html.P(f"Last Updated: {pd.to_datetime(unique_exo.releasedate.max()).strftime('%d %B %Y')}", style=tot_num_text_style_2)]),
], style=tot_num_section_style)

# Yearly discoveries line graph
n_exo_by_year = unique_exo['disc_year'].value_counts().sort_index().reset_index().rename(columns={'disc_year': 'Year', 'count': 'Number of Discoveries'})
yearly_discoveries_graph = px.line(n_exo_by_year, 
                                   x='Year', 
                                   y='Number of Discoveries',
                                   title='Exoplanet discoveries by year',
                                   markers=True,
                                   template='simple_white')
yearly_discoveries_graph.update_layout(yaxis_title=None)
yearly_discoveries_graph.update_yaxes(showgrid=True)
yearly_discoveries_graph.update_layout(xaxis_title=None)
yearly_discoveries_graph.update_layout(margin=dict(l=5, r=5, t=20, b=5))
yearly_discoveries_graph.update_layout(title={"yref": "paper","y" : 1,"yanchor" : "bottom", "xanchor": "center","x": 0.5})
yearly_discoveries_wrapper = dcc.Graph(figure=yearly_discoveries_graph,
                                        style={"height": "200px", "width": "50%"})



### Layout ###
overview_layout = html.Div([
    dbc.Card(
        dbc.CardBody([
            html.Div(children=[tot_num_exoplanets, yearly_discoveries_wrapper], style={"display": "flex", "justifyContent": "space-between"}),

                   ]
        , style=card_style)
    )
])


