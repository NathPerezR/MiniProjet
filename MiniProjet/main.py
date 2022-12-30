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
import graphs
import data

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

# Layout
app.layout = dbc.Container([
    db_title, 
    #db_information,
    dcc.Dropdown(data.annees.unique(),"2021", id='dropdown'), 
    
    # Graphs
    dcc.Graph(id='histogramme',
              figure=graphs.histogramme),    
    dcc.Graph(id='carte',
              figure=graphs.fig),
    html.Div(html.Iframe(id='map', srcDoc =open('map.html', 'r').read(), width='100%', height='400'))
    #colombie_geo_map.explore()
    ],className="dbc", fluid=True)

if __name__ == '__main__':
    app.run_server(debug=True)
    
