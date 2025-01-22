import requests

BASE_LLM_URL = "http://172.18.112.1:11434"

def process_pdfs(uploaded_pdfs, st):

    """Process and send uploaded PDFs to the backend."""

    backend_url = BASE_LLM_URL
    if not uploaded_pdfs:
        st.error("No files being uploaded")

    st.write("Processing PDFs, please wait")
    files = [file for file in uploaded_pdfs]
    response = requests.post(f"{backend_url}/api/upload-pdf", files=files, timeout=1000)
    if response.status_code == 200:
        st.success("Files were uploaded successfully, please go ahead and ask any questions")
    else:
        st.error("Failed to upload the files. Please check")
