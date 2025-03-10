import streamlit as st
from PIL import Image
import numpy as np 
import pandas as pd
import tensorflow as tf
from tensorflow import keras
 

from src.data_management import download_dataframe_as_csv
from src.machine_learning.predictive_analysis import (
                                                    load_model_and_predict,
                                                    resize_input_image,
                                                    plot_predictions_probabilities)

def page_powdery_mildew_detector_body():
    st.info(
        f'As part of the *business requirement 2*, the client is interested to know if a given '
        f'leaf sample image, is fungal-infected with Powdery Mildew or not'
        )

    st.write(
        f'You can download a set of fungal-infected and not healthy leaves for live prediction.'
        f'You can download the images from [here](https://www.kaggle.com/datasets/codeinstitute/cherry-leaves)'
    )

    st.write('---')
    #to upload images from the view and set it to upload multiple and allowed image type as '.jpg'  and '.png'image file formats.
    images_buffer = st.file_uploader('Upload leaf images. You may select more than one.', type=['png', 'jpg'], accept_multiple_files=True)

    if images_buffer is not None:
        df_report = pd.DataFrame([])
        for image in images_buffer:
            
            img_pil = (Image.open(image))
            st.info(f'Leaf image sample: **{image.name}**')
            img_array = np.array(img_pil)
            #st.image function to display a pil image onthe view and passing the image through the 3 functions to resize,predict,and plot proba.
            st.image(img_pil, caption=f"Image Size: {img_array.shape[1]}px width x {img_array.shape[0]}px height")

            version = 'v1'
            #Revises the functions the images have to pass through 
            resized_img = resize_input_image(img=img_pil, version=version)
            pred_proba, pred_class = load_model_and_predict(resized_img, version=version)
            plot_predictions_probabilities(pred_proba, pred_class)

            #Create a report with the predictions  and display the results in a table
            df_report = df_report.append({'Name': image.name, "Result": pred_class},
                                        ignore_index=True)

        if not df_report.empty:
            st.success('Analysis Report ')
            st.table(df_report)
            st.markdown(download_dataframe_as_csv(df_report), unsafe_allow_html=True)
