import streamlit as st
from clarifai.auth.helper import ClarifaiAuthHelper
from clarifai.client import create_stub
from clarifai.listing.lister import ClarifaiResourceLister
from clarifai.modules.css import ClarifaiStreamlitCSS
from google.protobuf import json_format, timestamp_pb2

st.set_page_config(layout="wide")
ClarifaiStreamlitCSS.insert_default_css(st)

# This must be within the display() function.
auth = ClarifaiAuthHelper.from_streamlit(st)
stub = create_stub(auth)
userDataObject = auth.get_user_app_id_proto()
lister = ClarifaiResourceLister(stub, auth.user_id, auth.app_id, page_size=16)
st.title("Simple example to list inputs")

with st.form(key="data-inputs"):
  mtotal = st.number_input(
      "Select number of inputs to view in a table:", min_value=10, max_value=100)
  submitted = st.form_submit_button('Submit')

if submitted:
  if mtotal is None or mtotal == 0:
    st.warning("Number of inputs must be provided.")
    st.stop()
  else:
    st.write("Number of inputs in table will be: {}".format(mtotal))

  # Stream inputs from the app
  all_inputs = []
  for inp in lister.inputs_generator():
    all_inputs.append(inp)

    if len(all_inputs) >= mtotal:
      break

  # Get some common stuff out of the inputs.
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