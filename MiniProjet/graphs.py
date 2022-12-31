# -*- coding: latin1 -*-
# Ensemble de graphiques

import plotly.express as px
#import folium
import data

# Victimes par année

histogramme = px.histogram(data.victimes, data.annees,
                           title="Victimes par année",
                           template='plotly_dark',
                           labels={ 
                                   "Mayor de 18 años":"Adulte",
                                   "Menor de 18 años":"Enfant"})
histogramme.update_layout(yaxis_title='Victimes')

# Choropleth

carte_choro = px.choropleth_mapbox(
        data.victimes_departement,
        geojson=data.colombie_geo_map,
        title='Victimes par departement',
        color='Victimes',
        locations='Departement',
        featureidkey="properties.NOMBRE_DPT",
        mapbox_style="carto-positron",
        zoom=3,
        center={'lat':4.577316, 'lon':-74.298973},
        range_color=[0, 3000]
    )
