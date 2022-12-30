# -*- coding: latin1 -*-
# Ensemble de données
import pandas as pd
import geopandas as gpd

# DataFrame
victimes = pd.read_json('https://www.datos.gov.co/resource/yhxn-eqqw.json?$limit=20000')
victimes.rename(columns={'departamento':'Departement','ano':'Année','rangoedad':"Groupes d'âge"}, inplace=True)
departements = victimes['Departement']
annees = victimes['Année']
# Nouvelle data Frame avec la quantité de victimes par departement
victimes_departement = victimes.groupby(['Departement']).size().reset_index(name='Victimes')

# Données Geographics

# pylint: disable-next=line-too-long
GEO_COLOMBIE = 'https://gist.githubusercontent.com/john-guerra/43c7656821069d00dcbc/raw/be6a6e239cd5b5b803c6e7c2ec405b793a9064dd/Colombia.geo.json'
GEO_COL= 'MGN_ANM_DPTOS.geojson'
colombie_geo_map = gpd.read_file(GEO_COLOMBIE)

# Latitud et Longitud du centre de la Colombie
colombie_centre = (4.577316, -74.298973)