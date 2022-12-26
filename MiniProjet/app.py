# Imports
from dash import Dash, html, dcc
#import dash_boostrap_component as dbc
import pandas as pd
import plotly.express as px
import folium
import geopandas
#import callbacks.py



# Data
victimes = pd.read_json('https://www.datos.gov.co/resource/yhxn-eqqw.json?$limit=30000')
departements = victimes['departamento']
annees = victimes['ano']

# Graphics
histogramme = px.histogram(victimes, annees, 
                           color_discrete_sequence=px.colors.qualitative.Pastel2, 
                           color=victimes['rangoedad'], 
                           title="Victimes par annee",
                           labels={'ano':'Annee'})
histogramme.update_layout(yaxis_title='Victimes')

#'xaxis': {'title': {'text': 'gdpPercap'}},
geo_colombie = "https://gist.githubusercontent.com/john-guerra/43c7656821069d00dcbc/raw/be6a6e239cd5b5b803c6e7c2ec405b793a9064dd/Colombia.geo.json"
coords = victimes[['latitudcabecera', 'longitudcabecera']]
colombie_centre = (4.577316, -74.298973)
map = folium.Map(location=colombie_centre, tiles='OpenStreetMap', zoom_start=6)
folium.GeoJson(
        data= geopandas.read_file(geo_colombie),
        name= 'Colombie'
    ).add_to(map)
map.save(outfile='map.html')



# Dashboard
app = Dash(__name__)

# Layout
app.layout = html.Div(children=[
    html.H1('Victimes de mines antipersonnel en Colombie',
            style={'textAlign': 'center'}),
    # Dropdown
    dcc.Dropdown(id='dropdown', options=annees.unique(), value="2021"),
    # Graphs
    dcc.Graph(id='histogramme',
              figure=histogramme),
    html.Iframe(id='map', srcDoc = open('map.html', 'r').read(), width='50%', height='300')
    ])


if __name__ == '__main__':
    app.run_server(debug=True)
    
