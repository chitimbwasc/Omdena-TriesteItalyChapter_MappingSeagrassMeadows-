import dash
from dash import dcc, html
import plotly.express as px
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
from graphs import graph_table

#################################################################################################
#                               LOAD_DATA
#################################################################################################





dash.register_page(__name__,
                   path='/machinelaerning',
                   name='Model Metrics',
                   title='New heatmaps',
                   image='pg3.png',
                   description='Learn all about the heatmap.'
)

layout = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.Dropdown(placeholder='Select metrics or params',options=['Metrics','Metrics & Parameters'],
                                     id='date_choice', value='Metrics & Parameters')
                    ], xs=10, sm=10, md=8, lg=4, xl=4, xxl=4
                )
                
            ]
        ),
        dbc.Row(
            [
                
                dbc.Col(
                    [
                        dcc.Graph(id='model_table')
                    ], width=4
                )

            ]
        )        


    ]
)

