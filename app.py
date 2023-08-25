import streamlit as st
from clarifai_utils.modules.css import ClarifaiStreamlitCSS

# If ClarifaiInputListing class is in a different module, import it:
# from your_module import ClarifaiInputListing

st.set_page_config(layout="wide")
ClarifaiStreamlitCSS.insert_default_css(st)

# Sidebar selection
options = ["Home", "List Inputs"]
choice = st.sidebar.selectbox("Choose a Page", options)

if choice == "Home":
    st.markdown("Please select a specific page from the sidebar to the left")
elif choice == "List Inputs":
    # Instantiate the ClarifaiInputListing class to run its logic.
    ClarifaiInputListing()


