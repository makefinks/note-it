import streamlit as st
import os
from PyPDF2 import PdfReader

st.set_page_config(page_title="NOTE IT", initial_sidebar_state="expanded")

model_options = ["claude-3-haiku-20240307", "claude-3-sonnet-20240229", "claude-3-opus-20240229"]

pricing = {
    "claude-3-sonnet-20240229":  [0.000003, 0.000015],
    "claude-3-opus-20240229": [0.000015, 0.000075],
    "claude-3-haiku-20240307": [0.00000025, 0.00000125]
}

st.header("Upload a file")

st.session_state.loaded_pdf = st.file_uploader("Upload a file", accept_multiple_files=False, type="pdf")

if st.session_state.loaded_pdf is not None:

    st.session_state.model = st.selectbox("Image Model", model_options)
    pdf_reader = PdfReader(st.session_state.loaded_pdf)
    num_pages = len(pdf_reader.pages)

    low_bound = (num_pages * pricing[st.session_state.model][0] * 1000) + num_pages * pricing[st.session_state.model][1] * 200
    high_bound = (num_pages * pricing[st.session_state.model][0] * 1000) + num_pages * pricing[st.session_state.model][1] * 500
    st.write(f"Estimated Price: {low_bound:.2g}—{high_bound:.2g}$ ({num_pages} pages)")

    # get page count of pdf


if st.button("Submit"):

    # set viewer flag to False
    st.session_state.convert_done = False

    # create temp folder if it doesnt exist
    if not os.path.exists("conversion/temp"):
        os.makedirs("conversion/temp")

    with open("conversion/temp/temp_input.pdf", "wb") as f:
        f.write(st.session_state.loaded_pdf.getbuffer())
    
    st.switch_page("pages/split_view.py")