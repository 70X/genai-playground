import streamlit as st
from pathlib import Path

# Path to your README.md
readme_path = Path(__file__).parent.parent / "README.md"

# Load and display README
if readme_path.exists():
    readme_content = readme_path.read_text(encoding="utf-8")
    st.markdown(readme_content, unsafe_allow_html=True)
else:
    st.write("README.md not found")
