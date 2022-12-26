#Imports
from dash import Dash, html, dcc 
#import dash_boostrap_component as dbc
import pandas as pd
import plotly.express as px

app = Dash(__name__)

#Data
victimes = pd.read_json('https://www.datos.gov.co/resource/yhxn-eqqw.json?$limit=50000')
departements = victimes['departamento']
annees = victimes['ano']
histogramme = px.histogram(victimes, departements, 
                           color_discrete_sequence=px.colors.qualitative.Pastel2, 
                           color=victimes['rangoedad'], 
                           title="Victimes par departement",
                           labels={'departamento':'Departement'})
histogramme.update_layout(yaxis_title='Victimes')

#Layout
app.layout = html.Div(children=[
    html.H1('Victimes de mines antipersonnel en Colombie',
            style={'textAlign': 'center'}),
    #Dropdown
    dcc.Dropdown(annees.unique(), "1993-2022"),
    #Graphs
    dcc.Graph(id='histogramme',
              figure=histogramme)
    ])

if __name__ == '__main__':
    app.run_server(debug=True)
