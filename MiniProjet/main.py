# -*- coding: latin1 -*-
# Imports

from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import graphs
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

# Dropdoxn Carte
dropdown_carte =  dcc.Dropdown(id='dropdown_carte',
        options=['Municipalité', 'Departement'],
        value='Departement', clearable=False
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
            html.P(data.top5_municipalite, id='top5_munn', className='card-text')
            ]
        )
    ], color='warning'
   )

#Graphs
db_annees_histogramme = dcc.Graph(id='histogramme', figure=graphs.histogramme)
db_carte = dcc.Graph(id='carte', figure= graphs.carte_choro),

#dbc.CaedGroup

# Layout
app.layout = dbc.Container([
    db_title, 
    # Cards
    dbc.CardGroup([card_total_victimes,card_top5_deptartements,card_top5_municip]),
    # Graphs
    dbc.Row([dbc.Col(card_victimes_pie),
             dbc.Col(db_carte)], justify='around'),
    #dropdown_carte,
    dbc.Row(dbc.Col(db_annees_histogramme))
    ],className='dbc')

@app.callback(
    Output('graph_pie', 'figure'), 
    Input('victimes_pie', 'value'))
def generate_pie(value):
    ''' 
    Creation d'un pie pour visualiser les pourcentage en fonction du type de victime ou de condition suite à l'incident
    '''
    fig = px.pie(data.victimes, names=data.victimes[value], hole=.5, template='plotly_dark', height=300)
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
    
