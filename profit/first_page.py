import streamlit as st
from clarifai.auth.helper import ClarifaiAuthHelper
from clarifai.client import create_stub
from clarifai.listing.lister import ClarifaiResourceLister
from clarifai.modules.css import ClarifaiStreamlitCSS
from google.protobuf import json_format, timestamp_pb2

class ClarifaiInputListing:
    def __init__(self):
        st.set_page_config(layout="wide")
        ClarifaiStreamlitCSS.insert_default_css(st)
        
        self.auth = ClarifaiAuthHelper.from_streamlit(st)
        self.stub = create_stub(self.auth)
        self.userDataObject = self.auth.get_user_app_id_proto()
        self.lister = ClarifaiResourceLister(self.stub, self.auth.user_id, self.auth.app_id, page_size=16)
        
        self.mtotal = 0
        
        self.display()

    def data_input_form(self):
        with st.form(key="data-inputs"):
            self.mtotal = st.number_input(
                "Select number of inputs to view in a table:", min_value=10, max_value=100)
            submitted = st.form_submit_button('Submit')
        return submitted

    def process_inputs(self):
        if self.mtotal is None or self.mtotal == 0:
            st.warning("Number of inputs must be provided.")
            st.stop()
        else:
            st.write("Number of inputs in table will be: {}".format(self.mtotal))

        all_inputs = []
        for inp in self.lister.inputs_generator():
            all_inputs.append(inp)

            if len(all_inputs) >= self.mtotal:
                break

        data = []
        for inp in all_inputs:
            data.append({
                "id": inp.id,
                "status": inp.status.description,
                "created_at": timestamp_pb2.Timestamp.ToDatetime(inp.created_at),
                "modified_at": timestamp_pb2.Timestamp.ToDatetime(inp.modified_at),
                "metadata": json_format.MessageToDict(inp.data.metadata),
            })

        st.dataframe(data)

    def display(self):
        st.title("Simple example to list inputs")
        if self.data_input_form():
            self.process_inputs()


if __name__ == "__main__":
    ClarifaiInputListing()

