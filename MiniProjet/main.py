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
victimes = pd.read_json('https://www.datos.gov.co/resource/yhxn-eqqw.json?$limit=20000')
departements = victimes['departamento']
annees = victimes['ano']

# Graphics

histogramme = px.histogram(victimes, annees,
                           #color_discrete_sequence=px.colors.qualitative.Pastel2,
                           color=victimes['rangoedad'],
                           title="Victimes par année",
                           template='plotly_dark',
                           labels={'ano':'Année', 'rangoedad':"Groupes d'âge", 
                                   "Mayor de 18 años":"Adulte",
                                   "Menor de 18 años":"Enfant"})
histogramme.update_layout(yaxis_title='Victimes')

# pylint: disable-next=line-too-long
GEO_COLOMBIE = 'https://gist.githubusercontent.com/john-guerra/43c7656821069d00dcbc/raw/be6a6e239cd5b5b803c6e7c2ec405b793a9064dd/Colombia.geo.json'
GEO_COL= 'MGN_ANM_DPTOS.geojson'
colombie_geo_map = gpd.read_file(GEO_COLOMBIE)

# Latitud et Longitud du centre de la Colombie
colombie_centre = (4.577316, -74.298973)
# Carte centrée en Colombie
colombie_carte = folium.Map(location=colombie_centre, zoom_start=5)

# Nouvelle data Frame avec la quantité de victimes par departement
victimes_departement = victimes.groupby(['departamento']).size().reset_index(name='Victimes')


choro = folium.Choropleth(
    geo_data = colombie_geo_map,
    data = victimes_departement, 
    columns = ['departamento', 'Victimes'],
    key_on="properties.NOMBRE_DPT",
    fill_color='YlOrRd',
    fill_opacity=0.8,
    name='Choropleth',
    legend_name = 'Victimes par departement',
    highlight=True,)
#.add_to(colombie_carte)
tooltipGeo=folium.features.GeoJsonTooltip(
        fields=['NOMBRE_DPT'],
        aliases=['Departement'],
        style=("background-color: white;"
               "color: #333333; font-size: 12px; padding: 10px;"))
#PopUp("{}\n".format(victimes_departement['departamento'], victimes_departement['Victimes'])).add_to(choro)
choro.geojson.tooltip = tooltipGeo

folium.GeoJson(data = colombie_geo_map, name='Hover',                
               tooltip=tooltipGeo).add_to(colombie_carte)
choro.add_to(colombie_carte)

#colombie_carte.add_child(hover)
#colombie_carte.keep_in_front(hover)
folium.raster_layers.TileLayer('OpenStreetMap', name='Open Street').add_to(colombie_carte)
folium.raster_layers.TileLayer('Stamen Terrain', name ='Stamen Terrain').add_to(colombie_carte)
folium.LayerControl().add_to(colombie_carte)
colombie_carte.save(outfile='map.html')


# Style bootstrap
dbc_css = 'https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css'
# Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY,dbc_css])

# HTML Components
db_title = html.H1('Victimes de mines antipersonnel en Colombie',
           className='bg-info p-2 mb-2 text-center')
# Infos
db_information = dbc.Card()
# Dropdown
#dropdown = 
fig = px.choropleth(
        victimes_departement,
        geojson=colombie_geo_map,
        color='Victimes',
        color_continuous_scale='deep',
        locations='departamento',
        featureidkey="properties.NOMBRE_DPT",
        projection="mercator",
        range_color=[0, 3000]        
    )
# Layout
app.layout = dbc.Container([
    db_title, 
    #db_information,
    dcc.Dropdown(annees.unique(),"2021", id='dropdown'), 
    
    # Graphs
    dcc.Graph(id='histogramme',
              figure=histogramme),    
    dcc.Graph(id='carte',
              figure=fig),
    html.Div(html.Iframe(id='map', srcDoc =open('map.html', 'r').read(), width='100%', height='400'))
    #colombie_geo_map.explore()
    ],className="dbc", fluid=True)

if __name__ == '__main__':
    app.run_server(debug=True)
    
