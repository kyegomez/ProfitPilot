import streamlit as st
# from clarifai_utils.modules.css import ClarifaiStreamlitCSS
from LlamaClarifaiChat import LlamaClarifaiChat  # Assuming LlamaClarifaiChat is in the same directory

st.set_page_config(layout="wide")
ClarifaiStreamlitCSS.insert_default_css(st)

# Sidebar selection
options = ["Home", "Chat"]
choice = st.sidebar.selectbox("Choose a Page", options)

if choice == "Home":
    st.markdown("Please select a specific page from the sidebar to the left")
elif choice == "Chat":
    # Instantiate the LlamaClarifaiChat class to run its logic.
    LlamaClarifaiChat()
