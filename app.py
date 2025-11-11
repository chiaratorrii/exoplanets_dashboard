from dash import Dash
from components.layout import layout
from data.fetch_data_function import fetch_exoplanet_tap

sql = "select pl_name,hostname,sy_snum,sy_pnum,sy_mnum,discoverymethod,disc_year,disc_facility,disc_instrument,pl_orbper,pl_rade,pl_radj,pl_masse,pl_massj,pl_dens,st_rad,st_mass,sy_dist,releasedate from ps"
exoplanets = fetch_exoplanet_tap(sql)

app = Dash(__name__)
app.title = "Exoplanets Dashboard"
app.layout = layout

if __name__ == "__main__":
    app.run(debug=True)