
import os
from sklearn.model_selection import train_test_split
from sklearn import linear_model, tree, neighbors
import numpy as np
import plotly.graph_objects as go
import plotly.colors as colors
from plotly.subplots import make_subplots
import dash
from dash import dcc, html, callback, Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
from datetime import datetime
import plotly.figure_factory as ff

import numpy as np
import mlflow
from mlflow.tracking import MlflowClient


#################################################################################################
#                               LOAD MODEL
#################################################################################################
# create a client to access the MLflow tracking server
client = MlflowClient()

#declare env variables 
os.environ['MLFLOW_TRACKING_USERNAME'] = 'emanuel.afessa'
os.environ['MLFLOW_TRACKING_PASSWORD'] = '48e371b32ba331dd7e83ea7a2418b33ee080845a' 
os.environ['MLFLOW_TRACKING_URI'] = 'https://dagshub.com/Omdena/TriesteItalyChapter_MappingSeagrassMeadows.mlflow'

#seet dagshub connection
mlflow.set_tracking_uri('https://dagshub.com/Omdena/TriesteItalyChapter_MappingSeagrassMeadows.mlflow')



#################################################################################################
#                               LOAD_DATA
#################################################################################################


# get the data after processing
df_rain = pd.read_csv('https://raw.githubusercontent.com/EmanuelAfessa/datasetsforml/main/df_rain_alg.csv')



#################################################################################################
#                               COMPUTE_ML_GRAPHS
#################################################################################################


################################################################################
#                               GRAPH 1 :indicator for predicted precipitation 
# using a ml model from mlflow model registry integrated to dagshub
################################################################################
##############################
# collect model from registry
#############################

# for model fetching purposes 
df = mlflow.search_runs(experiment_ids='0', max_results= 1, order_by=["metrics.accuracy DESC"])
run_id = df.loc[df['metrics.accuracy'].idxmax()]['run_id']
model = mlflow.keras.load_model("runs:/" + run_id + "/model")

# for visualisation purposes 
df2 = df.T



@callback(
    Output('model_table', 'figure'),
    Input('date_choice', 'value')
   

)


def update_graph(value):     
    

    fig = ff.create_table(df2, index=True)
  
    return fig











