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
