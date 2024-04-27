########################################################
# Goal : py classify pixels 
# Date : 29/02/2024
########################################################



#########################
# Import libraries 
#########################
import os 
import mlflow 
from mlflow.keras import *

import glob
import tifffile
import numpy as np

import base64
import dash
from dash import html
from dash.dependencies import Input, Output
from urllib.parse import quote as urlquote
from matplotlib import pyplot as plt
# import cv2
##############################################
#
# PART 1 : COMPUTATIONS 
# 
##############################################

##########################
# Get model from dagshub 
##########################
os.environ['MLFLOW_TRACKING_USERNAME'] = 'emanuel.afessa'
os.environ['MLFLOW_TRACKING_PASSWORD'] = '48e371b32ba331dd7e83ea7a2418b33ee080845a' 
os.environ['MLFLOW_TRACKING_URI'] = 'https://dagshub.com/Omdena/TriesteItalyChapter_MappingSeagrassMeadows.mlflow'

# set dagshub connection
mlflow.set_tracking_uri('https://dagshub.com/Omdena/TriesteItalyChapter_MappingSeagrassMeadows.mlflow')

# get best model 
df = mlflow.search_runs(experiment_ids='0',  order_by=["metrics.accuracy DESC"])
print('%%%%%%%%%%% DEST MODELS %%%%%%%%%%%%%%')
print(df.head())
print(df['tags.mlflow.source.name'].head())
run_id = df.loc[df['metrics.accuracy'].idxmax()]['run_id']
print(f'%%%%%%%%%%%%%%%%%%%% rund_id {run_id} %%%%%%%%%%%%%%%%%%%%%%%')
requirements = mlflow.artifacts.download_artifacts("runs:/" + run_id + "/model/requirements.txt")
print(requirements)
model = mlflow.pyfunc.load_model("runs:/" + run_id + "/model")
print('model import succesfull')



##############################################
#
# PART 2 :  DISPLAY
# 
##############################################

###############################
# upload images via user input 
###############################
#UPLOAD_DIRECTORY = "D:/Seagrass_webapp/graphs/uploads"
UPLOAD_DIRECTORY = "C:/omdena-projects/seagrass2024/dash_app/graphs/uploads"
def save_file(name, content):
    """Decode and store a file uploaded with Plotly Dash."""
    
    data = content.encode("utf8").split(b";base64,")[1]
    with open(os.path.join(UPLOAD_DIRECTORY, name), "wb") as fp:
        fp.write(base64.decodebytes(data))


def uploaded_files():
# first delect existing 
    """List the files in the upload directory."""
    files = []
    for filename in os.listdir(UPLOAD_DIRECTORY):
        path = os.path.join(UPLOAD_DIRECTORY, filename)
        if os.path.isfile(path):
            files.append(filename)
    return files


def file_download_link(filename):
    """Create a Plotly Dash 'A' element that downloads a file from the app."""
    location = "/download/{}".format(urlquote(filename))
    return html.A(filename, href=location)


@dash.callback(
    Output("file-list", "children"),
    [Input("upload-data", "filename"), Input("upload-data", "contents")],
)
def update_output(uploaded_filenames, uploaded_file_contents):
    # delete old before save new 
    filesToRemove = [os.path.join(UPLOAD_DIRECTORY,f) for f in os.listdir(UPLOAD_DIRECTORY)]
    for f in filesToRemove:
        os.remove(f) 
    """Save uploaded files and regenerate the file list."""

    if uploaded_filenames is not None and uploaded_file_contents is not None:
        for name, data in zip(uploaded_filenames, uploaded_file_contents):
            save_file(name, data)

    files = uploaded_files()
    if len(files) == 0:
        return [html.Li("No files yet!")]
    else:
        return [html.Li(file_download_link(filename)) for filename in files]


###############################################################################
#                               GRAPH  : display and classify  sentinel2 image
###############################################################################
@dash.callback(Output("output-image-upload","children"),
          Input("image-classify-btn","n_clicks"))



def update_output(n):
    if n:
        num_images = 10
        image_names = glob.glob("D:/Seagrass_webapp/graphs/uploads/*.tif")
        image_names.sort()
        image_names_subset = image_names[0:num_images]
        images = [tifffile.imread(image) for image in image_names_subset]
        image_dataset = np.array(images)
        print("Total images in the original dataset are: ", len(image_names))
        print("Image data shape is: ", image_dataset.shape)
        print("Max pixel value in image is: ", image_dataset.max())
        
        ##########################
        # Build X_test
        ##########################
        X_test = image_dataset.astype(np.float32)
        print('X_test successfull')

        ##########################
        # Make prediction
        ##########################
        y_pred = model.predict(X_test)
        y_pred_argmax = np.argmax(y_pred, axis=3)
        print(y_pred_argmax.shape)

        #####################################################
        # Plot prediction and original image and save to disk 
        #####################################################
        
        # put a for loop here : to loop in X_test and make as many predictions as there are images
        import random
        img_number = random.randint(0, len(X_test)-1)
        img = X_test[img_number]
        prediction = y_pred_argmax[img_number]

        plt.figure(figsize=(12, 8))
        band_index = 3  # Change this to the index of the band you want to display
        plt.subplot(231)
        # Display just one band of the image
        plt.imshow(img[:, :, band_index], cmap='gray')  # Replace 'gray' with any colormap you prefer
        plt.title('Original Image')  # Add a title indicating the band index (1-indexed)
        plt.subplot(232)
        plt.title('Prediction')
        plt.imshow(prediction)
        #plt.show()
        plt.savefig('D:/Seagrass_webapp/graphs/downloads/my_predcitions.png')

        #show the image on web 
        #DOWNLOAD_DIRECTORY = "D:/Seagrass_webapp/graphs/downloads"
        DOWNLOAD_DIRECTORY = "C:/omdena-projects/seagrass2024/dash_app/graphs/downloads"
        from PIL import Image
        image_root_path = DOWNLOAD_DIRECTORY
        returned_div = []
        for file in os.listdir(image_root_path):
            image_name = os.path.join(image_root_path,file)
            print(image_name)
            pil_image = Image.open(image_name)
            returned_div.append(html.Div([
            html.Img(src=pil_image)]))
        return returned_div










        