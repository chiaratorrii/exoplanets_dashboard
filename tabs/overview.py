from dash import html, dcc
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.express as px
from assets.py_style import *


# Load data
exoplanets = pd.read_csv("data\exoplanets_data.csv") 
unique_exo = exoplanets.sort_values(['pl_name', 'releasedate'], ascending=[True, False]).drop_duplicates(subset='pl_name', keep='first')


### Components ###

### Total number of exoplanets discovered section
tot_num_exoplanets = html.Div(children=[
    html.Br(),
    html.Div(id="total-exoplanets", children=[html.H1(len(unique_exo.pl_name.unique()))], style=tot_num_style),
    html.P("exoplanets discovered", style=tot_num_text_style_1),
    html.Div(id="last_update", children=[html.P(f"Last Updated: {pd.to_datetime(unique_exo.releasedate.max()).strftime('%d %B %Y')}", style=tot_num_text_style_2)]),
], style=tot_num_section_style)


### Yearly discoveries line graph
n_exo_by_year = unique_exo['disc_year'].value_counts().sort_index().reset_index().rename(columns={'disc_year': 'Year', 'count': 'Number of Discoveries'})
yearly_discoveries_graph = px.line(n_exo_by_year, 
                                   x='Year', 
                                   y='Number of Discoveries',
                                   title='Number of exoplanet discoveries by year',
                                   color_discrete_sequence=["#16425b"],
                                   markers=True,
                                   template='simple_white')
yearly_discoveries_graph.update_layout(yaxis_title=None)
yearly_discoveries_graph.update_yaxes(showgrid=True)
yearly_discoveries_graph.update_layout(xaxis_title=None)
yearly_discoveries_graph.update_layout(margin=dict(l=5, r=5, t=30, b=5))
yearly_discoveries_graph.update_xaxes(range=[1990, 2027])
yearly_discoveries_graph.update_layout(title={"yref": "container", "y":0.93 ,"yanchor" : "bottom", "xanchor": "center","x": 0.5, "font":{"color":"#16425b"}})

# Add shaded bands for 2014 and 2016 
yearly_discoveries_graph.add_vrect(
    x0=2013.5, x1=2014.5,
    fillcolor="#d5deff", opacity=0.5,
    layer="below", line_width=0,
    annotation_text="2014: Kepler data release",
    annotation_position="top right",
    annotation=dict(font_size=10, x=2013.48, y=0.64, showarrow=False, xanchor="right")
)
yearly_discoveries_graph.add_vrect(
    x0=2015.5, x1=2016.5,
    fillcolor="#d5deff", opacity=0.5,
    layer="below", line_width=0,
    annotation_text="2016: Improved statistical techniques",
    annotation_position="top left",
    annotation=dict(font_size=10, x=2016.52, y=0.98, showarrow=False, xanchor="left")
)
yearly_discoveries_wrapper = dcc.Graph(figure=yearly_discoveries_graph, responsive=True,
                                        style={"width": "55%", "height": "100%"})


### Number of stars donut chart
n_exo_by_stars = unique_exo['sy_snum'].value_counts().sort_index().reset_index()
n_stars_donut= px.pie(n_exo_by_stars,
                      names="sy_snum",
                      values="count",
                      color_discrete_sequence=['#16425b','#2f6690','#3a7ca5','#81c3d7'],
                      hole=0.6,
                      title="Planets by number of stars")
n_stars_donut.update_layout(title={"yref": "container", "y":0.93 ,"yanchor" : "bottom", "xanchor": "center","x": 0.5, "font":{"color":"#16425b"}},
                            showlegend=False 
                            )
n_stars_donut.update_layout(margin=dict(l=10, r=10, t=40, b=2))
# Update traces for percentage formatting and font size
n_stars_donut.update_traces(
    textinfo="percent+label", 
    texttemplate="%{label}: %{percent:.1%}", 
    textfont_size=10 
)
n_stars_donut_wrapper = dcc.Graph(figure=n_stars_donut, responsive=True,
                                        style={"width": "25%", "height": "100%"})


# ### Number of moons donut chart
# n_exo_by_moon = unique_exo['sy_mnum'].value_counts().sort_index().reset_index()
# n_moon_donut= px.pie(n_exo_by_moon,
#                       names="sy_mnum",
#                       values="count",
#                       color_discrete_sequence=['#16425b','#2f6690','#3a7ca5','#81c3d7'],
#                       hole=0.75,
#                       title="Planets by number of moons")
# n_moon_donut.update_layout(title={"yref": "container", "y":0.93 ,"yanchor" : "bottom", "xanchor": "center","x": 0.5},
#                             showlegend=False 
#                             )
# n_moon_donut.update_layout(margin=dict(l=15, r=15, t=40, b=5))
# # Update traces for percentage formatting and font size
# n_moon_donut.update_traces(
#     textinfo="percent+label", 
#     texttemplate="%{label}: %{percent:.1%}", 
#     textfont_size=10 
# )
# n_moon_donut_wrapper = dcc.Graph(figure=n_moon_donut,
#                                         style={"height": "200px", "width": "25%"})


### Histogram for distance
dist_hist= px.histogram(unique_exo,
                        x="sy_dist",
                        color_discrete_sequence=["#16425b"],
                        title='Number of exoplanets by distance',
                        template='simple_white')
dist_hist.update_layout(yaxis_title=None)
dist_hist.update_layout(xaxis_title=None)
dist_hist.update_layout(margin=dict(l=5, r=5, t=30, b=2))
dist_hist.update_layout(title={"yref": "container", "y":0.93 ,"yanchor" : "bottom", "xanchor": "center","x": 0.5, "font":{"color":"#16425b"}})
dist_hist.add_annotation(text="(in light years)", x=0.5, xref="paper", y=1.00, yref="paper", showarrow=False, font={"color": "gray", "size": 10}, align="center")
dist_hist_wrapper = dcc.Graph(figure=dist_hist, responsive=True,
                                        style={"width": "47%", "height": "100%"})


### Bar for top 5 discovery method
n_exo_by_method = unique_exo['discoverymethod'].value_counts().sort_index().reset_index().sort_values("count").tail(5)
method_bar= px.bar(n_exo_by_method,
                        x="count",
                        y="discoverymethod",
                        color_discrete_sequence=['#16425b'],
                        title='Number of exoplanets by top 5 discovery method',
                        template='simple_white',
                        orientation='h')
method_bar.update_layout(yaxis_title=None)
method_bar.update_layout(xaxis_title=None)
method_bar.update_layout(margin=dict(l=5, r=5, t=30, b=2))
method_bar.update_layout(title={"yref": "container", "y":0.93 ,"yanchor" : "bottom", "xanchor": "center","x": 0.5, "font":{"color":"#16425b"}})
method_bar_wrapper = dcc.Graph(figure=method_bar, responsive=True,
                                        style={"width": "47%", "height": "100%"})



### Layout ###
overview_layout = html.Div([
    dbc.Card(
        dbc.CardBody([
            html.Div(children=[tot_num_exoplanets, yearly_discoveries_wrapper, n_stars_donut_wrapper], 
                     style=half_card_section_style),
            html.Br(style={"margin":"5px", }),
            html.Br(style={"margin":"5px", "line-height":"50px"}),
            html.Div(children=[dist_hist_wrapper, method_bar_wrapper], 
                     style=half_card_section_style),

                   ],
                   style=card_body_style,
        ),
    style=card_style),
], style=overview_layout_style)


