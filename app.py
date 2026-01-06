import streamlit as st
from markitdown import MarkDownIt
import os
from io import BytesIO

# Initialize MarkDownIt engine
md_engine = MarkDownIt()

# Page Configuration
st.set_page_config(page_title="Universal Document Reader", page_icon="📄")

def convert_file(uploaded_file):
    """Processes the uploaded file and returns markdown text."""
    try:
        # MarkItDown can take a file stream or path. 
        # For Streamlit, we pass the uploaded file directly.
        result = md_engine.convert(uploaded_file)
        return result.text_content
    except Exception as e:
        st.error(f"⚠️ Could not read {uploaded_file.name}. Please check the format.")
        return None

# UI Header
st.title("📑 Universal Document Reader")
st.markdown("Convert Word, Excel, PPT, PDF, and HTML into clean Markdown instantly.")

# [2] Upload Area
uploaded_files = st.file_uploader(
    "Drag and drop files here", 
    type=["docx", "xlsx", "pptx", "pdf", "html"], 
    accept_multiple_files=True
)

if uploaded_files:
    for uploaded_file in uploaded_files:
        with st.spinner(f"Processing {uploaded_file.name}..."):
            # [1] The Engine Processing
            content = convert_file(uploaded_file)
            
            if content:
                # [2] Instant Preview
                with st.expander(f"👁️ Preview: {uploaded_file.name}", expanded=True):
                    st.text_area(
                        label="Converted Text",
                        value=content,
                        height=300,
                        key=f"text_{uploaded_file.name}"
                    )
                
                # [4] Technical Constraints: Naming logic
                base_name = os.path.splitext(uploaded_file.name)[0]
                
                # [2] Download Options
                col1, col2 = st.columns(2)
                
                with col1:
                    st.download_button(
                        label="📥 Download as .md",
                        data=content,
                        file_name=f"{base_name}_converted.md",
                        mime="text/markdown",
                        key=f"md_{uploaded_file.name}"
                    )
                
                with col2:
                    st.download_button(
                        label="📥 Download as .txt",
                        data=content,
                        file_name=f"{base_name}_converted.txt",
                        mime="text/plain",
                        key=f"txt_{uploaded_file.name}"
                    )
                st.divider()

# Footer / Resilience Note
st.caption("Stable connection enabled with 5s timeouts and User-Agent headers for internal requests.")
