# -*- coding: latin1 -*-
# Imports

from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import folium
import geopandas as gpd
import matplotlib.pyplot as plt
#import callbacks.py
import graphs
from graphs import generate_pie
import data

print('Recolection des données. Patientez...')

# Style bootstrap
dbc_css = 'https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css'
# Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.DARKLY,dbc_css])

# Title layout
db_title = html.H1('Victimes de mines antipersonnel en Colombie',
           className='bg-info p-2 mb-2 text-center')

# Dropdown Classification des Victimes 
options_dropdown = {'condicion':'Force Publique vs Civils', 
            "Groupes d'âge": "Groupes d'âge", 
            'estado':'Morts vs blessés',
            'genero':'Hommes vs Femmes'}
dropdown_pie =  dcc.Dropdown(id='victimes_pie',
        options= options_dropdown,
        value='condicion', clearable=False
    )

# Cartes Informatives
card_victimes_pie = dbc.Card(
    [
        dbc.CardBody([
        html.H4('Classification des Victimes', className='card-title text-center'),
        dropdown_pie,
        dcc.Graph(id='graph_pie'),
        html.P( '')]
        )
    ]
    )
card_total_victimes = dbc.Card(
    [
        dbc.CardBody([
            html.H4('Total des victimes', className='card-title text-center'),
            html.P(data.total_victimes,id ='total', className='card-text text-center')
            ]
        )
    ], color='danger'
    )
card_top5_deptartements = dbc.Card(
    [
        dbc.CardBody([
            html.H4('Les departements les plus affectés', className='card-title text-center'),
            html.P(data.top5_departements, id ='top5_dept', className='card-text')
            ]
        )
    ], color='warning'
    )
card_top5_municip = dbc.Card(
    [
        dbc.CardBody([
            html.H4('Les municipalitées les plus affectées', className='card-title text-center'),
            html.P('dep',id ='top5_munn', className='card-text')
            ]
        )
    ], color='warning'
   )

#Graphs
db_annees_histogramme = dcc.Graph(id='histogramme', figure=graphs.histogramme)
db_carte_dpt = dcc.Graph(id='carte', figure=graphs.carte_choro),
db_carte_folium = html.Iframe(id='map', srcDoc =open('map.html', 'r').read(), width='100%', height='400')

#dbc.CaedGroup

# Layout
app.layout = dbc.Container([
    db_title, 
    #Cards
    dbc.Row([dbc.Col(card_victimes_pie),
             dbc.Col([card_total_victimes,card_top5_deptartements,card_top5_municip])], justify='around'),
    #dcc.Dropdown(data.annees.unique(),'2021', id='dropdown'), 
    # Graphs
    dbc.Row([dbc.Col(db_annees_histogramme, width=6),
             #dbc.Col(db_carte_dpt),
             dbc.Col(db_carte_folium, width=5)], justify='around')
    ],className='dbc')

@app.callback(
    Output('graph_pie', 'figure'), 
    Input('victimes_pie', 'value'))
    #Input("values", "value"))
def generate_pie(value):
    if (str(value) == "Groupes d'âge"):
        label_replace = {'Mayor de 18 años':'Adulte','Menor de 18 años':'Enfant'}
    else:
        label_replace = None
    fig = px.pie(data.victimes, names=data.victimes[value], labels = label_replace, hole=.5, template='plotly_dark', height=300)
    return fig

#@app.callback(
#    Output("graph", "figure"), 
#    Input("candidate", "value"))
#def display_choropleth(candidate):
#    df = px.data.election() # replace with your own data source
#    geojson = px.data.election_geojson()

#    fig = px.choropleth_mapbox(
#        df, geojson=geojson, color=candidate,
#        locations="district", featureidkey="properties.district",
#        center={"lat": 45.5517, "lon": -73.7073}, zoom=9,
#        range_color=[0, 6500])
#    fig.update_layout(
#        margin={"r":0,"t":0,"l":0,"b":0},
#        mapbox_accesstoken=token)

#    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
    
