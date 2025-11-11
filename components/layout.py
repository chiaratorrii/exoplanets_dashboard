from dash import html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
from tabs.overview import overview_layout
from tabs.discovery_facilities import discovery_facilities_layout
from tabs.comparison import comparison_layout
from assets.py_style import *


# Components
header = html.Div(className="header", children=[
            html.Img(src="/assets/logo.png"),
            html.H1("Exoplanets Dashboard")])

tabs_selector = dcc.Tabs(id="tabs-selector", value='overview', style=tabs_styles, className="tabs-container",
                         children=[
                             dcc.Tab(label='Overview', value='overview', style=tab_style, selected_style=tab_selected_style),
                             dcc.Tab(label='Discovery facilities', value='discovery_facilities', style=tab_style, selected_style=tab_selected_style),
                             dcc.Tab(label='Compare to Earth', value='comparison', style=tab_style, selected_style=tab_selected_style)])

tab_content= html.Div(id='tab_blue_wrapper', style=tab_blue_container_style, children=[
    dbc.Card(id='tab_content', children=[])
    ])


# Layout
layout = [header,
          tabs_selector,
          tab_content]


# Callbacks
@callback(Output('tab_content', 'children'),
              Input('tabs-selector', 'value'))
def render_content(tab):
    if tab == 'overview':
        return overview_layout
    elif tab == 'discovery_facilities':
        return discovery_facilities_layout
    elif tab == 'comparison':
        return comparison_layout    
