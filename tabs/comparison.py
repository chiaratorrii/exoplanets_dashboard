from dash import html, dcc, dash_table, callback, Output, Input
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from assets.py_style import *
from datetime import date


# Load data
exoplanets = pd.read_csv("data\exoplanets_data.csv") 
unique_exo = exoplanets.sort_values(['pl_name', 'releasedate'], ascending=[True, False]).drop_duplicates(subset='pl_name', keep='first')


### Components ###

### Distance
distance_slider = html.Div(children=
    dbc.InputGroup(
        [
            dbc.InputGroupText('Distance (light years):', style={"margin-bottom":"15px", "margin-left":"10px"}),
            dcc.RangeSlider(
                min=0, 
                max=unique_exo.sy_dist.max(),  
                value=[unique_exo.sy_dist.min(), unique_exo.sy_dist.max()],  
                allowCross=False,
                tooltip={"placement": "bottom", "always_visible": False},
                id='distance_slider',
                marks = ({dist: str(dist) for dist in range(0, int(unique_exo.sy_dist.max()), 2000)})
            ),
        ],
        style={"display": "flex", "flex-direction":"column", "width":"80%"}
    ),
    style=filter_container_style)


### Discovery method
discovery_options=list(unique_exo.groupby('discoverymethod').count()['pl_name'].sort_values(ascending=False).index)
discovery_method_dropdown = html.Div(
    dbc.InputGroup(
        [
            dbc.InputGroupText('Discovery method:', style={"margin-bottom":"10px"}),
            dcc.Dropdown(
                id='discovery_method_dropdown',
                options=discovery_options,
                value=discovery_options[0],
                style=discovery_method_dropdown_style
            )
        ],
        style={"display": "flex", "flex-direction":"column"}
    ),
    style=filter_container_style)


### Discovery year start
discovery_year_picker = html.Div(
    dbc.InputGroup(
        [
            dbc.InputGroupText('Discovery year:', style={"margin-bottom":"10px"}),
            dcc.DatePickerRange(
                display_format='YYYY',
                end_date_placeholder_text='YYYY',
                start_date=date(1990, 1, 1),
                end_date=date(2027, 12, 31),
                id='discovery_year_picker',
                className="custom-date-picker",
                style=discovery_year_picker_style
            )
        ],
        style={"display": "flex", "flex-direction":"column"}
    ),
    style=filter_container_style)

### Table with list of exoplanets to select from
comp_table = html.Div(id='comp_table_wrapper',
                      children=
                        dash_table.DataTable(
                        id='comp_table',
                        data=[],
                        columns=[],
                        sort_action='native',
                        style_data_conditional=[],
                        row_selectable="single",
                        selected_rows=[],
                        editable=False,
                        cell_selectable=False,
                        css=[{"selector": ".show-hide", "rule": "display: none"}] 
), style={'marginTop': '10px', 'marginBottom': '5px', 'marginLeft':'0px', 'marginRight':'0px', 'paddingLeft':'40px', 'width':'35%'})


### Bubble plot
bubble_plot = html.Div(id='bubble_plot', children=[], style={'width':'100%', 'height':'60%'})

### Info about the planet
exo_info= html.Div(id='exo_info', children=[], style={'height':'40%'})


### Layout ###
comparison_layout = html.Div([
    dbc.Card(
        dbc.CardBody([
            html.Div(children=[distance_slider, discovery_method_dropdown, discovery_year_picker], style=filter_section_style),
            html.Br(),
            html.Div(children=[comp_table,
                               html.Div(children=[bubble_plot, exo_info], style=comp_selected_style)], 
                               style=comp_section_style)
        ], style=card_body_style
        ),
    style=card_style),
], style=overview_layout_style)




# Table maker function
def make_table(data, style_data_conditional, style_cell_conditional):
    return dash_table.DataTable(
            id='comp_table',
            data=data.to_dict('records'),
            columns=[{'id': c, 'name': c, 'hideable': True} for c in data.columns],
            sort_action='native',
            style_cell_conditional=style_cell_conditional,
            style_data_conditional=style_data_conditional,
            style_header={
                'backgroundColor': '#f5f7fa',
                'fontWeight': 'bold',
                'border':'0px solid grey'
                },
            style_table={
                'overflowX': 'auto',
                'width': '100%'  # Ensure table spans full width
            },
            style_data={
                'width': '100%'  # Ensure data spans full width
            },
            style_cell={'font_family': '"Inter", "Helvetica Neue", Arial, sans-serif', 'font_size': '14px'},
            selected_rows=[],
            editable=False,
            cell_selectable=False,
            row_selectable="single",
            style_as_list_view=True,
            page_size=10,
            css=[{"selector": ".show-hide", "rule": "display: none"}] 
        )
        




@callback(
    Output(component_id='comp_table_wrapper', component_property='children'),
    Input(component_id='tabs-selector', component_property='value'),
    Input(component_id='distance_slider', component_property='value'),
    Input(component_id='discovery_method_dropdown', component_property='value'),
    Input(component_id='discovery_year_picker', component_property='start_date'),
    Input(component_id='discovery_year_picker', component_property='end_date'),
)
def update_exo_table(tab, distance, method, start_date, end_date):
    if tab != 'comparison':
        raise PreventUpdate
    
    start_date=start_date[:4]
    end_date=end_date[:4]

    table_data=unique_exo[['pl_name', 'sy_dist', 'discoverymethod', 'disc_year']].rename({'pl_name':'Planet name'}, axis=1)

    # Filters
    table_data=table_data[(table_data['sy_dist'] >= float(distance[0])) & (table_data['sy_dist'] <= float(distance[1]))]
    table_data=table_data[table_data['discoverymethod']==method]
    table_data=table_data[(table_data['disc_year'] >= int(start_date)) & (table_data['disc_year'] <= int(end_date))] 

    table_data=table_data[["Planet name"]]

    style_data_conditional=[]
    style_cell_conditional=[
        {
            'if': {'column_id':'Planet name'},
            'textAlign': 'left'
            }
    ]
        
    table = make_table(table_data, style_data_conditional, style_cell_conditional)

    return table


@callback(
    Output(component_id='bubble_plot', component_property='children'),
    Input(component_id='tabs-selector', component_property='value'),
    Input(component_id='comp_table', component_property='data'),
    Input(component_id='comp_table', component_property='selected_rows')
)
def update_bubble_plot(tab, table_data, selected_rows):
    if tab != 'comparison':
        raise PreventUpdate
    
    exo_data = unique_exo[['pl_name', 'pl_radj']]


    if not selected_rows:  
        return html.P("🪐 Please select a planet")
    
    exo_data_selected = exo_data[exo_data['pl_name'] == table_data[selected_rows[0]]['Planet name']]

    # Construct the bubble plot DataFrame
    if pd.notna(exo_data_selected['pl_radj'].mean()):
        exo_rad = 10.95 * exo_data_selected['pl_radj'].mean()
    else:
        exo_rad = 7

    bubble_plot_df = pd.DataFrame({
        'planet': ['Earth', 'Jupiter', f"{exo_data_selected['pl_name'].unique()[0]}"], 
        'radius': [1, 10.95, exo_rad],
        'y':[1, 1, 1]
    })

    # Dynamically calculate x positions
    x_positions = [0]  # Start the first circle at x=0
    for i in range(1, len(bubble_plot_df)):
        # Distance between perimeters is equal to the sum of radii of consecutive circles
        distance_between_centers = bubble_plot_df["radius"][i-1] + bubble_plot_df["radius"][i]
        x_positions.append((x_positions[-1] + distance_between_centers)/2)

    bubble_plot_df["x"] = x_positions


    fig = px.scatter(
    bubble_plot_df,
    x="x",  # X-axis
    y="y",  # Y-axis
    size="radius",  # Bubble size
    color="planet",  # Color of bubbles
    text='planet',
    hover_name="planet",  # Hover info
    hover_data={'planet': False, 'radius':False, 'x':False, 'y':False},
    # title="Exoplanet dimension",
    size_max=100,
    color_discrete_sequence=['#2f6690', '#FF7F50', '#ffcc00'],
    opacity=1,
    template='simple_white')

    fig.add_annotation(x=bubble_plot_df['x'][1], y=1, text=f"10.9 times <br> bigger than Earth", showarrow=False, font=dict(color='#16425b', size=14))
    if pd.isna(exo_data_selected['pl_radj'].mean()):
        fig.add_annotation(x=bubble_plot_df['x'][2], y=1, text="? times <br> bigger than Earth", showarrow=False, font=dict(color='#16425b', size=14))
    else:
        fig.add_annotation(x=bubble_plot_df['x'][2], y=1, text=f"{round(bubble_plot_df['radius'][2], 1)} times <br> bigger than Earth", showarrow=False, font=dict(color='black', size=14))


    fig.update_layout(yaxis_title=None)
    fig.update_layout(xaxis_title=None)
    fig.update_xaxes(showline=False, showticklabels=False, ticks="inside", tickwidth=0, tickcolor='white', ticklen=0)
    fig.update_yaxes(showline=False, showticklabels=False, ticks="inside", tickwidth=0, tickcolor='white', ticklen=0)
    fig.update_traces(textposition='bottom center')
    fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))
    fig.update_layout(title={"yref": "container", "y":0.93 ,"yanchor" : "bottom", "xanchor": "center","x": 0.5, "font":{"color":"#16425b"}},
                      showlegend=False)

    bubble_plot=dcc.Graph(figure=fig, responsive=True, style={'width':'100%'})

    # Return the bubble_plot_df as a string inside an html.P element
    return bubble_plot


@callback(
    Output(component_id='exo_info', component_property='children'),
    Input(component_id='tabs-selector', component_property='value'),
    Input(component_id='comp_table', component_property='data'),
    Input(component_id='comp_table', component_property='selected_rows')
)
def update_bubble_plot(tab, table_data, selected_rows):
    if tab != 'comparison':
        raise PreventUpdate
    
    if not selected_rows:  
        return html.P(" ")
    
    exo_data_selected = unique_exo[unique_exo['pl_name'] == table_data[selected_rows[0]]['Planet name']]
    
    pl_name = html.Div(children=[html.H2(exo_data_selected['pl_name'].unique()[0])],
                       style={'width':'30%', 'height':'100%', 'padding':'15px', 'display':'flex', 'align-items': 'center'})
    
    sy_info = html.Div(children=[
        html.P([
            html.B("System: "), html.Br(), 
            exo_data_selected['hostname'].unique()[0]]),
        html.P([
            html.B("Number of stars: "), html.Br(), 
            exo_data_selected['sy_snum'].unique()[0]]),
        html.P([
            html.B("Distance from solar system: "), html.Br(), 
            exo_data_selected['hostname'].unique()[0]])
    ], style={'width': '35%', 'height': '100%', 'padding':'15px'})

    disc_info = html.Div(children=[
        html.P([
            html.B("Discovery year: "), html.Br(), 
            exo_data_selected['disc_year'].unique()[0]]),
        html.P([
            html.B("Discovery facility: "), html.Br(), 
            exo_data_selected['disc_facility'].unique()[0]]),
        html.P([
            html.B("Discovery method: "), html.Br(), 
            exo_data_selected['discoverymethod'].unique()[0]])
    ], style={'width': '30%', 'height': '100%', 'padding':'15px'})

    return html.Div([pl_name,sy_info,disc_info], style=info_style)




