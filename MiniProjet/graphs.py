# -*- coding: latin1 -*-
# Ensemble de graphiques

import plotly.express as px
import folium
import data

# Victimes par année

histogramme = px.histogram(data.victimes, data.annees,
                           #color_discrete_sequence=px.colors.qualitative.Pastel2,
                           #color=data.victimes["Groupes d'âge"],
                           title="Victimes par année",
                           template='plotly_dark',
                           labels={ 
                                   "Mayor de 18 años":"Adulte",
                                   "Menor de 18 años":"Enfant"})
histogramme.update_layout(yaxis_title='Victimes')

# Creation d'un pie pour visualiser les pourcentage en fonction du type de victime ou de condition suite à l'incident
def generate_pie(type_victime):
    #if (type_victime == "Groupes d'âge"):
    #    label_replace = {'Mayor de 18 años':'Adulte'}
    #else:
    #    label_replace = {'Menor de 18 años':'Enfant'}
    fig = px.pie(data.victimes, names=type_victime, hole=.5)
    return fig

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


# Carte centrée en Colombie
colombie_carte = folium.Map(location=data.colombie_centre, zoom_start=3, tiles=None)

choro = folium.Choropleth(
    geo_data = data.colombie_geo_map,
    data = data.victimes_departement, 
    columns = ['Departement', 'Victimes'],
    key_on="properties.NOMBRE_DPT",
    fill_color='YlOrRd',
    fill_opacity=0.8,
    name='Choropleth',
    legend_name = 'Total de victimes par departement',
    highlight=True,)
#.add_to(colombie_carte)
tooltipGeo=folium.features.GeoJsonTooltip(
        fields=['NOMBRE_DPT'],
        aliases=['Departement'],
        style=("background-color: white;"
               "color: #333333; font-size: 12px; padding: 10px;"))
#PopUp("{}\n".format(victimes_departement['departamento'], victimes_departement['Victimes'])).add_to(choro)
choro.add_to(colombie_carte)

folium.GeoJson(data = data.colombie_geo_map, name='Hover',                
               tooltip=tooltipGeo).add_to(colombie_carte)


#colombie_carte.add_child(hover)
#colombie_carte.keep_in_front(hover)
folium.raster_layers.TileLayer('OpenStreetMap', name='Open Street').add_to(colombie_carte)
folium.raster_layers.TileLayer('Stamen Terrain', name ='Stamen Terrain').add_to(colombie_carte)
folium.LayerControl().add_to(colombie_carte)
colombie_carte.save(outfile='map.html')