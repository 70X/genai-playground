import requests
import streamlit as st

st.title("Chat Image")

if "messages_image" not in st.session_state:
    st.session_state.messages_image = []

for message in st.session_state.messages_image:
    with st.chat_message(message["role"]):
        st.image(message["content"])

if prompt := st.chat_input("Write your prompt in this input field"):
    # Show a temporary spinner while request is in flight
    with st.spinner("Assistant is thinking... Please don't switch the page"):
        response = requests.get(
            "http://localhost:8000/generate/image", params={"prompt": prompt}
        )
        response.raise_for_status()
        assistant_reply = response.content

    st.session_state.messages_image.append(
        {"role": "assistant", "content": assistant_reply}
    )
    with st.chat_message("assistant"):
        st.text("Here is your generated image")
        st.image(assistant_reply)
