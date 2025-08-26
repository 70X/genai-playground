import re
import requests
import streamlit as st

st.title("Chat 3D")

if "messages_3d" not in st.session_state:
    st.session_state.messages_3d = []

for message in st.session_state.messages_3d:
    with st.chat_message(message["role"]):
        st.download_button(
            label=f"Download file: {message['filename']}",
            data=message["content"],
            file_name=message["filename"],
            mime="text/plain",
        )

if prompt := st.chat_input("Write your prompt in this input field"):
    # Show a temporary spinner while request is in flight
    with st.spinner("Assistant is thinking... Please don't switch the page"):
        response = requests.get(
            "http://localhost:8000/generate/3d", params={"prompt": prompt}
        )
        response.raise_for_status()
        assistant_reply = response.content

    safe_name = re.sub(r"[^A-Za-z0-9_]", "", prompt[:20].replace(" ", "_"))
    filename = f"{safe_name}.obj"
    st.session_state.messages_3d.append(
        {
            "role": "assistant",
            "content": assistant_reply,
            "filename": filename,
        }
    )

    with st.chat_message("assistant"):
        st.text("Here is your generated 3D Image")
        st.download_button(
            label=f"Download file: {filename}",
            data=assistant_reply,
            file_name=filename,
            mime="text/plain",
        )
