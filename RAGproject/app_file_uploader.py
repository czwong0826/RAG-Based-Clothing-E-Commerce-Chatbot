
import streamlit as st  # type: ignore
from knowledge_base import KnowledgeBaseService
import time 

# add website title
st.title("Knowledge Base Uploader")

uploader_file = st.file_uploader(
    "Upload your knowledge base txt file here",
    type=["txt"],
    accept_multiple_files=False, #only allow one file to be uploaded
)

# Initialize the knowledge base service, and only create once per session to avoid re-initialization
if "service" not in st.session_state:   
    st.session_state["service"] = KnowledgeBaseService()

if uploader_file is not None:
    file_name = uploader_file.name
    file_type = uploader_file.type
    file_size = uploader_file.size/1024 # convert to KB
    st.subheader(f"File Name: {file_name}")
    st.write(f"Format:{file_type} | Size:{file_size:.2f} KB")
    #get_value -> bytes -> decode to string 
    text = uploader_file.getvalue().decode("utf-8") # read the file content
    #st.write(text)

    with st.spinner("Uploading..."):
        time.sleep(1)  # Simulate a delay for the upload process
        result = st.session_state["service"].upload_by_str(text, file_name)
        st.write(result)