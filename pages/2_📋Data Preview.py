import streamlit as st
import pandas as pd
import pydeck as pdk
from urllib.error import URLError
import os
import tempfile

def file_selector(folder_path='Data'):
    filenames = os.listdir(folder_path)
    selected_filename = st.selectbox('Select a file', filenames)
    return os.path.join(folder_path, selected_filename)



st.set_page_config(page_title="Data Preview", page_icon="Images/data.png")

st.markdown("<h1 style='text-align: center; color: white;'>Data Preview</h1>", unsafe_allow_html=True)

if len(os.listdir('Data')) == 0:
    st.markdown("<h2 style='text-align: center; color: white;'>Data is not present upload it in Chat Bot.</h2>", unsafe_allow_html=True)

else:
    filename = file_selector()
    if 'csv' in filename:    
        dt = pd.read_csv(filename)
    elif 'xlsx' in filename:
        dt = pd.read_excel(filename)
    values = st.slider(
        'Select a range of values',
        1.0, float(len(dt)), (0.0, float(len(dt))))
    dt.iloc[int(values[0]):int(values[1])]