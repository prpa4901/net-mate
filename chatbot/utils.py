import requests
import json

BASE_LLM_URL = "http://host.docker.internal:11434"

def upload_process_pdfs(uploaded_pdfs):

    """Process and send uploaded PDFs to the backend."""

    for uploaded_file in uploaded_pdfs:
        # Convert Streamlit's UploadedFile to a tuple format that requests can use
        # The key 'files' must match your FastAPI parameter name
        file_content = uploaded_file.read()
        uploaded_file.seek(0)  # Reset file pointer   
        files = {
            'file': (uploaded_file.name, file_content, 'application/pdf')
        }
        response = requests.post("http://backend-app:8087/pdf/upload/", files=files, timeout=1000)
        if response.status_code == 200:
            response = requests.post(
                f"http://backend-app:8087/embeddings/create-user-embeddings/?file_name={uploaded_file.name}",
                timeout=1000
            )
            if response.status_code == 200:
                return True

def conversation_interface(user_question):

    """Interface for the conversation with the backend."""

    headers = {'Content-Type': 'application/json'}

    payload = {"question": user_question}
    response = requests.post('http://backend-app:8087/llm/ask-query/',
                            headers=headers,
                            data=json.dumps(payload),
                            timeout=10000)
    if response.status_code == 200:
        response = response.json()
        return response['response']
    else:
        return "Failed to get the response. Please try again"


