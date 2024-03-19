import streamlit as st
from code_editor import code_editor

st.set_page_config(page_title="Viewer", layout="wide", initial_sidebar_state="collapsed")

st.header("Markdown Editor")
st.session_state.content = st.text_area("Enter Markdown", height=400)


if st.button("Print Markdown"):
    st.write(st.session_state.content)