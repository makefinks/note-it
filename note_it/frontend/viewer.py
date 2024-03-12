import streamlit as st
import os

st.set_page_config(page_title="NOTE IT", initial_sidebar_state="collapsed")

model_options = ["claude-3-sonnet-20240229", "claude-3-opus-20240229"]

st.header("Upload a file")

st.session_state.loaded_pdf = st.file_uploader("Upload a file", accept_multiple_files=False)

if st.session_state.loaded_pdf is not None:
    st.selectbox("Image Model", model_options, key="model")
    
if st.button("Submit"):

    # create temp folder if it doesnt exist
    if not os.path.exists("conversion/temp"):
        os.makedirs("conversion/temp")

    with open("conversion/temp/temp_input.pdf", "wb") as f:
        f.write(st.session_state.loaded_pdf.getbuffer())
    
    st.switch_page("pages/split_view.py")