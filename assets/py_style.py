### TABS SELECTOR STYLES ###

# Container style for dcc.Tabs
tabs_styles = {
    "backgroundColor": "#f5f7fa",  # container background
    "padding": "0px",
    "marginBottom": "0px"
}

# Style for individual tabs (normal/unselected)
tab_style = {
    "backgroundColor": "#d5deff",
    "color": "#002244",            # label color
    "borderRadius": "12px 12px 0 0",  # rounded top corners
    "marginLeft": "2px",
    "marginRight": "2px",
    "marginBottom": "0px",
    "borderBottom": "0px",
    "borderTop": "0px",
    "transition": "background-color 0.2s, color 0.2s",
    "padding":"10px"
}

# Style for selected tab
tab_selected_style = {
    "backgroundColor": "#003366",  # selected background
    "color": "#ffffff",            # selected label color
    "marginLeft": "2px",
    "marginRight": "2px",
    "marginBottom": "0px",
    "borderTop": "0px",
    "borderRadius": "12px 12px 0 0",  # rounded top corners
    "padding":"10px"
}

### TAB STYLE ###

tab_blue_container_style = {
    "backgroundColor": "#003366",
    "margin":"0px",
    "padding": "10px",
    }

tab_white_container_style = {
    "backgroundColor": "#ffffff"
    }

### CARD STYLE ###
overview_layout_style = {
    "height": "84.5vh",  # Full viewport height
    "display": "flex",
    "flexDirection": "column",
    "justifyContent": "space-between",
}

card_style = {
    "height": "100%",  # Card fills its parent container
    "display": "flex",  # Use flexbox for layout
    "flexDirection": "column",  # Arrange children vertically
    "justifyContent": "space-between",  # Space out children proportionally
    "margin": "10px",
    "padding": "15px",
    "boxShadow": "0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19)",
    "borderRadius": "12px",
    "backgroundColor": "#ffffff"
}

card_body_style = {
    "height": "100%",  # Card fills its parent container
    "display": "flex",  # Use flexbox for layout
    "flexDirection": "column",  # Arrange children vertically
    "justifyContent": "space-between",  # Space out children proportionally
}


### OVERVIEW TAB STYLES ###
tot_num_section_style = {
    "margin": "0px",
    "padding": "10px 10px 10px 10px",
    "textAlign": "center",
    "width": "20%",
    "height":"100%",
    "display": "flex",  # Use flexbox for layout
    "flexDirection": "column",  # Arrange children vertically
    "alignItems": "center",  # Vertically align items in the center
    "justifyContent": "center"
}
tot_num_style = {"fontSize": "30px", "fontWeight": "1200", "margin": "0px", "padding":"0px","color":"#16425b"}
tot_num_text_style_1 = {"font-weight":"bold", "fontSize": "18px", "margin": "2px", "color":"#16425b"}
tot_num_text_style_2 = {"fontSize": "10px", "color": "gray", "margin": "2px"}

yearly_discoveries_wrapper_style = {"width": "50%", "padding": "10px"}

half_card_section_style = {
    "display": "flex",  # Use flex layout for children
    "justifyContent": "space-between",  # Space children evenly
    "height": "50%",  # Each section takes half the height of the card
}

### COMPARISON TAB STYLES ###

filter_container_style={
        'margin-left': '10px',
        'width': '32%',
        'padding': '10px 0',
        'display': 'flex',
        'verticalAlign': 'middle',
        "justify-content":"space-around"
    }

discovery_method_dropdown_style={"border":"0px", "backgroundColor": "#f5f7fa", "width":"300px"}

discovery_year_picker_style={"border":"0px", "background-color": "#f5f7fa", "padding":"0px"}

filter_section_style = {
    "display": "flex",  # Use flex layout for children
    "justifyContent": "space-between",  # Space children evenly
    "height": "15%",  # Each section takes half the height of the card,
    'width':'100%'
}

comp_section_style = {
    "display": "flex",
    "height": "85%",
    "width": "100%",                # Ensure full width
    "padding": "0",                 # Remove padding
    "margin": "0",                   # Remove margins
    "display": "flex",  # Use flexbox for layout
    "flexDirection": "row",  # Arrange children verticall
}

comp_selected_style= {
    "display": "flex",
    "height": "85%",
    "width": "65%",                 
    "margin": "0",                  
    "display": "flex",  # Use flexbox for layout
    "flexDirection": "column",  # Arrange children verticall
    'paddingLeft':'30px', 
    'paddingRight':'30px', 
}

info_style = {
    "display": "flex",
    "height": "100%",
    "width": "100%",                 
    "margin": "0",                  
    "display": "flex",  # Use flexbox for layout
    "flexDirection": "row",  # Arrange children vertically
}