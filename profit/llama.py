# In this section, we set the user authentication, user and app ID, model details, and the URL of 
# the text we want as an input. Change these strings to run your own example.
######################################################################################################
######################################################################################################

from clarifai_grpc.channel.clarifai_channel import ClarifaiChannel
from clarifai_grpc.grpc.api import resources_pb2, service_pb2, service_pb2_grpc
from clarifai_grpc.grpc.api.status import status_code_pb2
import streamlit as st

# Your PAT (Personal Access Token) can be found in the portal under Authentification
PAT = st.secrets.PAT
# Specify the correct user_id/app_id pairings
# Since you're making inferences outside your app's scope
USER_ID = "n7o37rpzserv"
APP_ID = 'Llama2'
# Change these to whatever model and text URL you want to use
WORKFLOW_ID = 'Llama2'
TEXT_FILE_URL = 'https://samples.clarifai.com/negative_sentence_12.txt'

############################################################################
# YOU DO NOT NEED TO CHANGE ANYTHING BELOW THIS LINE TO RUN THIS EXAMPLE
############################################################################

def get_response(prompt):
    channel = ClarifaiChannel.get_grpc_channel()
    stub = service_pb2_grpc.V2Stub(channel)

    metadata = (('authorization', 'Key ' + PAT),)

    userDataObject = resources_pb2.UserAppIDSet(user_id=USER_ID, app_id=APP_ID)

    response = ""  # save response from the model

    post_workflow_results_response = stub.PostWorkflowResults(
        service_pb2.PostWorkflowResultsRequest(
            user_app_id=userDataObject,  
            workflow_id=WORKFLOW_ID,
            inputs=[
                resources_pb2.Input(
                    data=resources_pb2.Data(
                        text=resources_pb2.Text(
                            raw=prompt
                        )
                    )
                )
            ]
        ),
        metadata=metadata
    )

    if post_workflow_results_response.status.code != status_code_pb2.SUCCESS:
        print(post_workflow_results_response.status)

        return response

    # We'll get one WorkflowResult for each input we used above. Because of one input, we have here one WorkflowResult
    results = post_workflow_results_response.results[0]

    # Each model we have in the workflow will produce one output.
    for output in results.outputs:
        model = output.model

        print("Predicted concepts for the model `%s`" % model.id)
        for concept in output.data.concepts:
            print("	%s %.2f" % (concept.name, concept.value))

        response += output.data.text.raw + "\n"

    # Uncomment this line to print the full Response JSON
    # print(results)
    print(response)


import streamlit as st
from streamlit_chat import message
import profit.llama as llama

class LlamaClarifaiChat:
    
    def __init__(self):
        self.init_session_state()
        self.title = "Profit Pilot"
        self.render()

    def init_session_state(self):
        if "messages" not in st.session_state:
            st.session_state["messages"] = [{"role": "assistant", "content": "Say something to get started!"}]

    def clear_chat(self):
        st.session_state.messages = [{"role": "assistant", "content": "Say something to get started!"}]

    def chat_form(self):
        with st.form("chat_input", clear_on_submit=True):
            a, b = st.columns([4, 1])

            user_prompt = a.text_input(
                label="Your message:",
                placeholder="Type something...",
                label_visibility="collapsed",
            )

            b.form_submit_button("Send", use_container_width=True)
        return user_prompt

    def process_user_prompt(self, user_prompt):
        st.session_state.messages.append({"role": "user", "content": user_prompt})
        message(user_prompt, is_user=True)

        response = llama.get_response(user_prompt)
        msg = {"role": "assistant", "content": response}
        st.session_state.messages.append(msg)
        message(msg["content"])

    def render_messages(self):
        for msg in st.session_state.messages:
            message(msg["content"], is_user=msg["role"] == "user")

    def render_clear_chat_button(self):
        if len(st.session_state.messages) > 1:
            st.button('Clear Chat', on_click=self.clear_chat)

    def render(self):
        st.title(self.title)
        user_prompt = self.chat_form()
        self.render_messages()
        if user_prompt:
            self.process_user_prompt(user_prompt)
        self.render_clear_chat_button()


if __name__ == "__main__":
    LlamaClarifaiChat()
