
#################################################################################################
# pages.py are simply the receptors for the graphs. They only have the dropdown element and box to receive the graph
# there is no computation here. It is just a shell  
#                               
#################################################################################################

import dash
from dash import dcc, html, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.graph_objects as go

from graphs import graph_class_pixel




#################################################################################################
#                               LOAD_LAYOUT
#################################################################################################

# To create meta tag for each page, define the title, image, and description.
dash.register_page(__name__,
                   path='/',  # '/' is home page and it represents the url
                   name='Pixel Classification',  # name of page, commonly used as name of link
                   title='Pixel Classification',  # title that appears on browser's tab
                   image='pg1.png',  # image in the assets folder
                   description='Sentinel2 imageclassification'
)


layout = html.Div(children=[
                                    
                                    html.Br(),
                                    html.Div(children=[
                                        html.H3(children=" Mapping Seagrass Meadows"),
                                        html.P("This app uses a deep learning model to classify sentinel2 satellite images pixels into seagrass or no seagrass classes "),
                                        html.H6("Upload images"),
                                        # html.Div([
                                        #     "Select an Image:",
                                        #     dcc.Dropdown(id="image-dropdown",
                                        #     options=[{'label': i, 'value': os.path.join(IMAGE_DATASET_HOME,i)} for i in imagefiles_list])
                                        # ]),
                                        
                                        dcc.Upload(
                                        id="upload-data",
                                        children=html.Div(
                                            ["Drag and drop or click to select a file to upload."]
                                        ),
                                        style={
                                            "width": "80%",
                                            "height": "60px",
                                            "lineHeight": "60px",
                                            "borderWidth": "1px",
                                            "borderStyle": "dashed",
                                            "borderRadius": "5px",
                                            "textAlign": "center",
                                            "margin": "10px",
                                        },
                                        multiple=True,
                                    ),
                                    html.H6("Uploaded Files List"),
                                    html.Ul(id="file-list"),
                                        dbc.Button("Classify", color="warning", className="me-1",id="image-classify-btn"),
                                        html.Div(id="output-image-upload")
                                        
                                    ],style={"margin":"10px"}),  
                            ],
                            )


















