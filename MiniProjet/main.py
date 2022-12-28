# -*- coding: latin1 -*-
# Imports
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import folium
import geopandas as gpd
import matplotlib.pyplot as plt
#import callbacks.py



# Data
victimes = pd.read_json('https://www.datos.gov.co/resource/yhxn-eqqw.json?$limit=30000')
departements = victimes['departamento']
annees = victimes['ano']

# Graphics

histogramme = px.histogram(victimes, annees,
                           color_discrete_sequence=px.colors.qualitative.Pastel2,
                           color=victimes['rangoedad'],
                           title="Victimes par année",                           
                           labels={'ano':'Année', 'rangoedad':"Groupes d'âge", 
                                   "Mayor de 18 años":"Adulte",
                                   "Menor de 18 años":"Enfant"})
histogramme.update_layout(yaxis_title='Victimes')

#'xaxis': {'title': {'text': 'gdpPercap'}},
# pylint: disable-next=line-too-long
GEO_COLOMBIE = 'https://gist.githubusercontent.com/john-guerra/43c7656821069d00dcbc/raw/be6a6e239cd5b5b803c6e7c2ec405b793a9064dd/Colombia.geo.json'
GEO_COL= 'MGN_ANM_DPTOS.geojson'
colombie_geo_map = gpd.read_file(GEO_COLOMBIE)

colombie_centre = (4.577316, -74.298973)
colombie_carte = folium.Map(location=colombie_centre, tiles='OpenStreetMap', zoom_start=5)


departements1 = victimes.groupby('departamento').size().reset_index(name='Victimes')
#folium.GeoJson(
#        data= geopandas.read_file(GEO_COLOMBIE),
#        name= 'Colombie'
#    )
folium.Choropleth(
    geo_data = colombie_geo_map,
    data = departements1, 
    columns = ['departamento', 'Victimes'],
    key_on="properties.NOMBRE_DPT",
    fill_color="YlGn",
    legend_name = 'Victimes par departement').add_to(colombie_carte)


hover=folium.features.GeoJson(data = colombie_geo_map,
               tooltip=folium.features.GeoJsonTooltip(
        fields=['NOMBRE_DPT'],
        aliases=['Departement'],
        style=("background-color: white;"
               "color: #333333; font-size: 12px; padding: 10px;")))

colombie_carte.add_child(hover)
colombie_carte.keep_in_front(hover)
colombie_carte.save(outfile='map.html')


# Style bootstrap
dbc_css = 'https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css'
# Dashboard
app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY, dbc_css])

# HTML Components
db_title = html.H1('Victimes de mines antipersonnel en Colombie',
           className='bg-secondary p-2 mb-2 text-center')
# Dropdown
#dropdown = 
fig = px.choropleth(
        departements1,
        geojson=colombie_geo_map,
        color='Victimes',
        locations='departamento',
        featureidkey="properties.NOMBRE_DPT",
        projection="mercator",
        range_color=[0, 3000],
    )
# Layout
app.layout = dbc.Container([
    db_title, 
    dcc.Dropdown(id='dropdown', options=annees.unique(), value="2021"), 
    
    # Graphs
    dcc.Graph(id='histogramme',
              figure=histogramme),    
    dcc.Graph(id='carte',
              figure=fig),
    html.Div(html.Iframe(id='map', srcDoc =open('map.html', 'r').read(),title="folium iFrame", width='100%', height='400'))
    #colombie_geo_map.explore()
    ],className="dbc")
print(departements.value_counts())
print(departements1)

if __name__ == '__main__':
    app.run_server(debug=True)
    
