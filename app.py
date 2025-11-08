from dash import Dash
from components.layout import layout

app = Dash(__name__)
app.title = "Exoplanets Dashboard"
app.layout = layout

if __name__ == "__main__":
    app.run(debug=True)