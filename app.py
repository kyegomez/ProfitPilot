import streamlit as st
from clarifai_utils.modules.css import ClarifaiStreamlitCSS

st.set_page_config(layout="wide")

ClarifaiStreamlitCSS.insert_default_css(st)

st.markdown("Please select a specific page from the sidebar to the left")
