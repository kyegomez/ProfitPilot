import streamlit as st
from streamlit_chat import message
import llama

def clear_chat():
    st.session_state.messages = [{"role": "assistant", "content": "Say something to get started!"}]


st.title("Llama2 Clarifai Tutorial")


if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Say something to get started!"}]


with st.form("chat_input", clear_on_submit=True):
    a, b = st.columns([4, 1])

    user_prompt = a.text_input(
        label="Your message:",
        placeholder="Type something...",
        label_visibility="collapsed",
    )

    b.form_submit_button("Send", use_container_width=True)


for msg in st.session_state.messages:
    message(msg["content"], is_user=msg["role"] == "user")


if user_prompt:

    print('user_prompt: ', user_prompt)

    st.session_state.messages.append({"role": "user", "content": user_prompt})
    
    message(user_prompt, is_user=True)

    response = llama.get_response(user_prompt)  # get response from llama2 API (in our case from Workflow we created before)

    msg = {"role": "assistant", "content": response}

    print('st.session_state.messages: ', st.session_state.messages)

    st.session_state.messages.append(msg)

    print('msg.content: ', msg["content"])

    message(msg["content"])


if len(st.session_state.messages) > 1:
    st.button('Clear Chat', on_click=clear_chat)
