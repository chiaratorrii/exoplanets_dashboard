from dash import html, dcc, callback, Output, Input
from tabs.overview import overview_layout
from tabs.comparison import comparison_layout
from tabs.exo_of_the_day import exo_of_the_day_layout

# Components
header = html.Div(className="header", children=[
            html.Img(src="/assets/logo.png"),
            html.H1("Exoplanets Dashboard")])

tabs_selector = dcc.Tabs(id="tabs-selector", value='overview', className="tabs-container",
                         children=[
                             dcc.Tab(label='Overview', value='overview'),
                             dcc.Tab(label='Compare to Earth', value='comparison'),
                             dcc.Tab(label='Exoplanet of the day', value='exo_of_the_day'),])

tab_content= html.Div(id='tab_content', children=[])


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
    elif tab == 'comparison':
        return comparison_layout    
    elif tab == 'exo_of_the_day':
        return exo_of_the_day_layout