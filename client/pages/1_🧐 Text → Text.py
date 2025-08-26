import requests
import streamlit as st

st.title("Chat Text")

if "messages_text" not in st.session_state:
    st.session_state.messages_text = []

for message in st.session_state.messages_text:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Write your prompt in this input field"):
    st.session_state.messages_text.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Show a temporary spinner while request is in flight
    with st.spinner("Assistant is thinking... Please don't switch the page"):
        response = requests.get(
            "http://localhost:8000/generate/text", params={"prompt": prompt}
        )
        response.raise_for_status()
        assistant_reply = response.text

    st.session_state.messages_text.append(
        {"role": "assistant", "content": assistant_reply}
    )
    with st.chat_message("assistant"):
        st.markdown(assistant_reply)
