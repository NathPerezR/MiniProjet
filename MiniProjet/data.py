# -*- coding: latin1 -*-
# Ensemble de donn�es
import pandas as pd
import geopandas as gpd

# DataFrame
victimes = pd.read_json('https://www.datos.gov.co/resource/yhxn-eqqw.json?$limit=20000')
total_victimes = len(victimes.index)
victimes.rename(columns={'departamento':'Departement','municipio':'Municipalit�','ano':'Ann�e','rangoedad':"Groupes d'�ge"}, inplace=True)

annees = victimes['Ann�e']

# Nouvelle data Frame avec la quantit� de victimes par departement
victimes_departement = victimes.groupby(['Departement']).size().reset_index(name='Victimes')
victimes_departement.sort_values(by=['Victimes'], ascending=False, inplace=True)
top5_departements = victimes_departement['Departement'].head()
# Nouvelle data Frame avec la quantit� de victimes par municipalit�
victimes_municipalite = victimes.groupby(['Municipalit�']).size().reset_index(name='Victimes')
victimes_municipalite.sort_values(by=['Victimes'], ascending=False, inplace=True)
top5_municipalite = victimes_municipalite['Municipalit�'].head()

# Donn�es Geographics
# pylint: disable-next=line-too-long
GEO_COLOMBIE = 'https://gist.githubusercontent.com/john-guerra/43c7656821069d00dcbc/raw/be6a6e239cd5b5b803c6e7c2ec405b793a9064dd/Colombia.geo.json'
#GEO_COL= 'MGN_ANM_DPTOS.geojson'
colombie_geo_map = gpd.read_file(GEO_COLOMBIE)

# Latitud et Longitud du centre de la Colombie
colombie_centre = (4.577316, -74.298973)