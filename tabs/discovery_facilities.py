from dash import html, dcc, callback, Output, Input, dash_table
from dash.exceptions import PreventUpdate
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.express as px
from assets.py_style import *


all_observatories=pd.read_csv('data/observatories_exoplanets_geolocated.csv').drop('Name', axis=1).rename(columns={'disc_facility':'Name', 
                                                                                                                    'pl_name':'N of discovered planets',
                                                                                                                    'Established':'Year of Establishment'})
all_observatories.fillna('Unknown', inplace=True)
all_observatories['note']=all_observatories['note'].replace('Unknown', '')


### Filters ###

### Earth or space filter
earth_space_options=['Earth', 'Space']
earth_space_dropdown = html.Div(
    dbc.InputGroup(
        [
            dbc.InputGroupText('Facility location:', style={"margin-bottom":"10px","margin-top":"10px"}),
            dcc.Dropdown(
                id='earth_space_dropdown',
                options=earth_space_options,
                value=earth_space_options[0],
                style=earth_space_options_style
            )
        ],
        style={"display": "flex", "flex-direction":"column",'margin-left':'30px'}
    ),
    style={})



### Components ###

### Map of earth facilities
obs_earth=all_observatories[all_observatories['type']=='earth'].copy()
obs_earth['Latitude']=obs_earth['geolocation'].apply(lambda x: float(x.strip("()").split(", ")[0]))
obs_earth['Longitude']=obs_earth['geolocation'].apply(lambda x: float(x.strip("()").split(", ")[1]))
obs_earth['Year of Establishment']=[x.split('.')[0] for x in obs_earth['Year of Establishment']]

earth_map = px.scatter_mapbox(
    obs_earth,
    lat="Latitude",
    lon="Longitude",
    hover_name="Name",
    hover_data={"Location": True, "Latitude":False, "Longitude":False, "note":False, "Year of Establishment": False, "N of discovered planets": False, "Link":False},
    zoom=0,
    color_discrete_sequence=["#2f6690"],
    size_max=15,
    # height=600,
)

earth_map.update_layout(
    mapbox_style="carto-positron",  # You can use other styles like "open-street-map"
    mapbox_center={"lat": 30.0, "lon": 10.0},
    mapbox_zoom=1,
    margin={"l": 0, "r": 0, "t": 0, "b": 0},
)

earth_map_div=html.Div(children=[dcc.Graph(id='earth_map', figure=earth_map, style={'height': '100%'})], style={'width':'70%', 'height':'100%'})
facility_info_earth=html.Div(id='facility_info_earth', children=[], style={'width':'25%', 'height':'100%', 'margin-left':'20px', 'margin-right':'20px'})
earth_div=html.Div(children=[earth_map_div, facility_info_earth], style={"display": "flex","flexDirection": "row", "height":"100%"})

### Space facilities
obs_space=all_observatories[all_observatories['type']=='space'].copy()
obs_space['Year of Establishment']=[x.split('.')[0] for x in obs_space['Year of Establishment']]
obs_space=obs_space.sort_values(by='N of discovered planets', ascending=False)
obs_space['Name']='🚀 ' + obs_space['Name']


space_table = children=dash_table.DataTable(
                        id='space_table',
                        data=obs_space[['Name']].to_dict('records'),
                        columns=[{'id': c, 'name': c, 'hideable': True} for c in obs_space[['Name']].columns],
                        sort_action='native',
                        style_cell_conditional=[{'if': {'column_id':'Name'},'textAlign': 'left'}],
                        style_data_conditional=[],
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

space_table_div=html.Div(id='space_table_div', children=[space_table], style={'width':'50%', 'height':'100%', 'marginTop': '10px', 'marginBottom': '5px', 'marginLeft':'0px', 'marginRight':'0px', 'paddingLeft':'30px'})
facility_info_space=html.Div(id='facility_info_space', children=[], style={'width':'35%', 'height':'100%', 'margin-left':'40px', 'margin-right':'20px'})
space_div=html.Div([space_table_div, facility_info_space],style={"display": "flex","flexDirection": "row", 'justifyContent': 'space-between'})

### Map or space div
map_or_space=html.Div(id='map_or_space', children=[], style={'width':'100%', 'height':'100%'})


### Facility info



### Layout ###
discovery_facilities_layout= html.Div([
    dbc.Card(
        dbc.CardBody([
            html.Div(children=[earth_space_dropdown], style=filter_section_style_facilities),
            html.Br(),
            html.Div(children=[map_or_space], style=map_or_space_style), 
        ], style=card_body_style
        ),
    style=card_style),
], style=overview_layout_style)




@callback(
    Output(component_id='map_or_space', component_property='children'),
    Input(component_id='tabs-selector', component_property='value'),
    Input(component_id='earth_space_dropdown', component_property='value')
)
def update_earth_or_space(tab, earth_or_space):
    if tab != 'discovery_facilities':
        raise PreventUpdate
    
    if earth_or_space=='Earth':
        return earth_div
    else:
        return space_div


### Callbacks ###

@callback(
    Output(component_id='facility_info_earth', component_property='children'),  # Update the facility info Div
    Input(component_id='earth_map', component_property='clickData')  # Listen for clicks on the map
)
def display_selected_point(click_data):
    if click_data is None:
        return html.P(f"🔭 Please select a telescope on the map")
        # raise PreventUpdate  # Prevent updates if no point is clicked
    
    # print(click_data)
    
    # Extract information about the clicked point
    point_info = click_data['points'][0]  # Get the first point
    name = point_info['hovertext']  # Extract the hover text (facility name)
    lat = point_info['lat']  # Extract latitude
    lon = point_info['lon']  # Extract longitude
    custom_data = point_info['customdata']  # Extract custom data, e.g., Year of Opening and City

    notes=html.P(f"⚠️ Note: {custom_data[3]}") if custom_data[3]!='' else html.P()

    # Format and return the information for display
    return html.Div(
         dbc.Card(
            dbc.CardBody([
        html.H2(f"{name}"),
        html.P(f"📍 Location: {custom_data[0]}"),
        html.P(f"🗺️ Coordinates: {custom_data[1]}, {custom_data[2]}"),
        notes,
        html.P(f"⌛ Establishment: {custom_data[4]}"),
        html.P(html.A("🔗 More info", href=custom_data[6], target="_blank", 
                style={"color": "#2f6690",  "text-decoration": "none"})),
        html.Br(),
        html.Br(),
        html.Div([html.H2(f"{custom_data[5]}🪐", style={"font-size": "40px", "justify-content": "center", "display": "flex"}),
        html.P("number of discovered planets", style={"font-size": "12px", "display": "flex", "justify-content": "center"})])
    ]), style=obs_card_earth_style))


@callback(
    Output(component_id='facility_info_space', component_property='children'),  # Update the facility info Div
    Input(component_id='space_table', component_property='data'),
    Input(component_id='space_table', component_property='selected_rows')
)
def display_selected_point(table_data, selected_rows):
    if len(selected_rows)==0:
        return html.P(f"🚀 Please select a telescope")
        # raise PreventUpdate  # Prevent updates if no point is clicked
        
    
    selected_obs = obs_space[obs_space['Name'] == table_data[selected_rows[0]]['Name']]

    # print(click_data)
    
    # notes=html.P(f"⚠️ Note: {custom_data[3]}") if custom_data[3]!='' else html.P()
    location=selected_obs['Location'].values[0] if selected_obs['Location'].values[0]!='Unknown' else 'Space'

    # Format and return the information for display
    return html.Div(
        dbc.Card(
            dbc.CardBody([
                html.H2(f"{selected_obs['Name'].values[0][2:]}"),
                html.P(f"📍 Location: {location}"),
                # notes,
                html.P(f"⌛ Establishment: {selected_obs['Year of Establishment'].values[0]}"),
                html.P(html.A("🔗 More info", href=selected_obs['Link'].values[0], target="_blank", 
                        style={"color": "#2f6690",  "text-decoration": "none"})),
                html.Br(),
                html.Br(),
                html.Div([html.H2(f"{selected_obs['N of discovered planets'].values[0]}🪐", style={"font-size": "40px", "justify-content": "center", "display": "flex"}),
                html.P("number of discovered planets", style={"font-size": "12px", "display": "flex", "justify-content": "center"})])
    ]), style=obs_card_space_style))