import streamlit as st
from markitdown import MarkItDown
import os

# Initialize MarkItDown engine
md_engine = MarkItDown()

# Page Configuration
st.set_page_config(page_title="Universal Document Reader", page_icon="📄")

def convert_file(uploaded_file):
    try:
        # markitdown processes the uploaded file stream
        result = md_engine.convert(uploaded_file)
        return result.text_content
    except Exception as e:
        st.error(f"⚠️ Could not read {uploaded_file.name}. Please check the format.")
        return None

def format_bytes(size):
    """Convert bytes to a human-readable format."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0

# UI Header
st.title("📑 Universal Document Reader")
st.markdown("Convert documents into clean Markdown and compare file efficiency.")

# Upload Area
uploaded_files = st.file_uploader(
    "Drag and drop files here", 
    type=["docx", "xlsx", "pptx", "pdf", "html"], 
    accept_multiple_files=True
)

if uploaded_files:
    for uploaded_file in uploaded_files:
        with st.spinner(f"Processing {uploaded_file.name}..."):
            content = convert_file(uploaded_file)
            
            if content:
                # Calculate Sizes
                original_size = uploaded_file.size
                converted_size = len(content.encode('utf-8'))
                
                # Percentage Calculation
                reduction = ((original_size - converted_size) / original_size) * 100
                
                # Tabs for Preview and Analytics
                tab1, tab2 = st.tabs(["📄 Preview & Download", "📊 File Size Comparison"])
                
                with tab1:
                    st.text_area(
                        label=f"Preview: {uploaded_file.name}",
                        value=content,
                        height=250,
                        key=f"text_{uploaded_file.name}"
                    )
                    
                    base_name = os.path.splitext(uploaded_file.name)[0]
                    col1, col2 = st.columns(2)
                    with col1:
                        st.download_button(
                            "📥 Download .md", content, f"{base_name}_converted.md", "text/markdown", key=f"md_{uploaded_file.name}"
                        )
                    with col2:
                        st.download_button(
                            "📥 Download .txt", content, f"{base_name}_converted.txt", "text/plain", key=f"txt_{uploaded_file.name}"
                        )

                with tab2:
                    st.subheader("Efficiency Metrics")
                    
                    # Create the Table
                    data = {
                        "File State": ["Original File", "Converted Text"],
                        "Size": [format_bytes(original_size), format_bytes(converted_size)]
                    }
                    st.table(data)
                    
                    # Show percentage improvement
                    if reduction > 0:
                        st.success(f"✨ Text version is **{reduction:.1f}% smaller** than the original.")
                    else:
                        st.info("The text version is roughly the same size as the original.")
                
                st.divider()

st.caption("Resilient conversion powered by MarkItDown and Streamlit.")
