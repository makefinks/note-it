import streamlit as st
import base64
from note_it.conversion.convert import convert
import streamlit.components.v1 as components
import asyncio
st.set_page_config(page_title="Viewer", layout="wide", initial_sidebar_state="collapsed")
columns = st.columns(2)

with columns[0]:

    st.header("Original PDF")
    base64_pdf = base64.b64encode(st.session_state.loaded_pdf.read()).decode('utf-8')
    # Embedding PDF in HTML
    pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="600" height="1000" type="application/pdf"></iframe>'
    # Displaying File
    st.markdown(pdf_display, unsafe_allow_html=True)

with columns[1]:

    st.header("Converted Markdown")
    # convert pdf to markdown and display
    with st.spinner("Converting PDF to markdown..."):
        convert_success = asyncio.run(convert("conversion/temp/temp_input.pdf", model_name=st.session_state.model))
        print(f"convert_success: {convert_success}")

    if convert_success:

        scrollable_container_css = """
            <style>
            .scrollable-container {
                overflow: auto;
                height: 1000px; /* Adjust the height as needed */
            }
            </style>
        """

        st.session_state.converted_markdown = open("final.md", "r").read()
        
        st.markdown(scrollable_container_css, unsafe_allow_html=True)

        scrollable_markdown = f'<div class="scrollable-container">{st.session_state.converted_markdown}</div>'
        
        # Display the scrollable markdown content
        st.markdown(scrollable_markdown, unsafe_allow_html=True)

if "converted_markdown" in st.session_state:
    st.download_button(
        label="Download Markdown",
        data=st.session_state.converted_markdown,
        file_name="converted_markdown.md",
        mime="text/markdown",
    )
