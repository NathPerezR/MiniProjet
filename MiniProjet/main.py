# Imports
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
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
                           #color_discrete_sequence=px.colors.qualitative.Pastel2,
                           color=victimes['rangoedad'],
                           title="Victimes par annee",
                           nbins=20,
                           labels={'ano':'Annee'})
histogramme.update_layout(yaxis_title='Victimes')

#'xaxis': {'title': {'text': 'gdpPercap'}},
# pylint: disable-next=line-too-long
GEO_COLOMBIE = 'https://gist.githubusercontent.com/john-guerra/43c7656821069d00dcbc/raw/be6a6e239cd5b5b803c6e7c2ec405b793a9064dd/Colombia.geo.json'
GEO_COL= 'MGN_ANM_DPTOS.geojson'
#coords = victimes[['latitudcabecera', 'longitudcabecera']]
#colombie_centre = (4.577316, -74.298973)
#colombie_carte = folium.Map(location=colombie_centre, tiles='OpenStreetMap', zoom_start=6)
folium.GeoJson(
        data= geopandas.read_file(GEO_COLOMBIE),
        name= 'Colombie'
    ).add_to(colombie_carte)
colombie_carte.save(outfile='map.html')

colombie_geo_map = geopandas.read_file(GEO_COLOMBIE)
# Style bootstrap
dbc_css = 'https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css'
# Dashboard
app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY, dbc_css])

# HTML Components
db_title = html.H1('Victimes de mines antipersonnel en Colombie')
           # className='bg-primary text-white p-2 mb-2 text-center')
# Dropdown
#dropdown = 
fig = px.choropleth(
        victimes,
        geojson=geopandas.read_file(GEO_COLOMBIE),
        color=departements.value_counts(),
        locations=departements.value_counts(),
        featureidkey="properties.NOMBRE_DPT",
        projection="mercator",
        range_color=[0, 2000],
    )
# Layout
app.layout = dbc.Container([
    db_title, 
    dcc.Dropdown(id='dropdown', options=annees.unique(), value="2021"),
    
    
    # Graphs
    dcc.Graph(id='histogramme',
              figure=histogramme),
    #html.Iframe(id='map', srcDoc = open('map.html', 'r').read(), width='50%', height='300'),
    dcc.Graph(id='carte',
              figure=fig)
    #colombie_geo_map.explore()
    ],className="dbc")


if __name__ == '__main__':
    app.run_server(debug=True)
