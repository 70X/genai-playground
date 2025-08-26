import requests
import streamlit as st

st.title("Chat Video")

if "messages_video" not in st.session_state:
    st.session_state.messages_video = []

for message in st.session_state.messages_video:
    with st.chat_message(message["role"]):
        st.video(message["content"])

if uploaded_file := st.file_uploader("Choose an image", type=["png", "jpg", "jpeg"]):
    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
    image_bytes = uploaded_file.read()
    files = {"image": ("uploaded_image.png", image_bytes)}
    # Show a temporary spinner while request is in flight
    with st.spinner("Assistant is thinking... Please don't switch the page"):
        response = requests.post("http://localhost:8000/generate/video", files=files)
        response.raise_for_status()
        assistant_reply = response.content

    st.session_state.messages_video.append(
        {"role": "assistant", "content": assistant_reply}
    )

    with st.chat_message("assistant"):
        st.text("Here is your generated Video")
        st.video(assistant_reply)
