import requests
import json

BASE_LLM_URL = "http://host.docker.internal:11434"

def upload_process_pdfs(uploaded_pdfs):

    """Process and send uploaded PDFs to the backend."""

    files = [file for file in uploaded_pdfs]
    response = requests.post("http://backend:8087/pdf/upload", files=files, timeout=1000)
    if response.status_code == 200:
        response = requests.post("http://backend:8087/embeddings/create-user-embeddings/",
                                 timeout=1000)
        if response.status_code == 200:
            return True

def conversation_interface(user_question,
                           chat_history = None):

    """Interface for the conversation with the backend."""

    headers = {'Content-type': 'application/json'}

    if chat_history:
        chat_history = _convert_chat_history_to_string(chat_history)
    payload = {"question": user_question,
                "chat_history": chat_history}
    response = requests.post('http://backend:8087/llm/ask-query/',
                            headers=headers,
                            data=json.dumps(payload),
                            timeout=1000)
    if response.status_code == 200:
        response = response.json()
        return response['response']
    else:
        return "Failed to get the response. Please try again"


def _convert_chat_history_to_string(chat_history):
    """Convert chat history to string format."""
    chat_history_str = ""
    for chat in chat_history:
        chat_history_str += f"User: {chat['question']}\nBot: {chat['response']}\n"
    return chat_history_str

