import requests
import streamlit as st

st.title("Chat Audio")

if "messages_audio" not in st.session_state:
    st.session_state.messages_audio = []

for message in st.session_state.messages_audio:
    with st.chat_message(message["role"]):
        content = message["content"]
        if isinstance(content, bytes):
            st.audio(content)
        else:
            st.markdown(content)

if prompt := st.chat_input("Write your prompt in this input field"):
    # Show a temporary spinner while request is in flight
    with st.spinner("Assistant is thinking... Please don't switch the page"):
        response = requests.get(
            "http://localhost:8000/generate/audio", params={"prompt": prompt}
        )
        response.raise_for_status()
        assistant_reply = response.content

    st.session_state.messages_audio.append(
        {"role": "assistant", "content": assistant_reply}
    )
    with st.chat_message("assistant"):
        st.text("Here is your generated audio")
        st.audio(assistant_reply)
