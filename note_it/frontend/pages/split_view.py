import os
import streamlit as st
from note_it.conversion.convert import convert
import streamlit.components.v1 as components
import asyncio
from PIL import Image


st.set_page_config(page_title="Viewer", layout="wide", initial_sidebar_state="expanded")
columns = st.columns(2)

if st.session_state.loaded_pdf is None:
    st.warning("No PDF file uploaded. Please upload a PDF File on the upload page.")
    st.stop()

if "convert_done" not in st.session_state:
    st.session_state.convert_done = False

if st.session_state.convert_done is False:
    with st.spinner("Converting PDF to Markdown..."):
        st.session_state.convert_done = asyncio.run(convert())

if st.session_state.convert_done:
    
    # get the markdown files from the output folder
    markdown_files = os.listdir("output")
    # sort the markdown files based on the page number
    markdown_files.sort(key=lambda x: int(x.split("_")[-1].split(".")[0]))

    image_files = os.listdir("images")
    image_files.sort(key=lambda x: int(x.split("_")[-1].split(".")[0]))
    
    # display the markdown files in containers that fit the size of the images
    for index, file in enumerate(markdown_files):

        with st.container(height=800):

            columns = st.columns([0.25, 0.75])

            with columns[0]:
                st.image(f"images/{image_files[index]}")

            with columns[1]:
                with open(f"output/{file}", "r", encoding="utf-8") as f:
                    #response_dict = code_editor(f.read(), lang="markdown")
                    st.write(f.read())


if "converted_markdown" in st.session_state:

    columns = st.columns(3)

    with columns[0]:
            st.download_button(
            label="Download Markdown ✅",
            data=st.session_state.converted_markdown,
            file_name="converted_markdown.md",
            mime="text/markdown",
            use_container_width=True
        )
    with columns[1]:
        if st.button("Fix Headings 🪄", use_container_width=True):
            pass

    with columns[2]:
        if st.button("Rerun 🔁", use_container_width=True):
            st.session_state.convert_done = False
            st.rerun()


   
   
