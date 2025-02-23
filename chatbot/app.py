import streamlit as st
from langchain.embeddings import HuggingFaceInstructEmbeddings
from langchain_community.embeddings import OllamaEmbeddings
from utils import conversation_interface, upload_process_pdfs


# User and bot images
USER_IMAGE = "/app/static/images/your-image.png"  # Replace with your image path
BOT_IMAGE = "/app/static/images/bot-image.png"  # Replace with bot image path


if __name__ == "__main__":

    st.set_page_config(page_title="Net-Mate", page_icon="🧠", layout="wide")
    st.title(
        "Welcome to Net-Mate, your network assistant buddy,you can upload any PDFs or text docs"
        )

    user_question = st.text_input("Ask me anything about networking queries as per uploaded docs")

    if st.button("Submit"):
        if not user_question:
            st.error("Please enter a valid question")
        else:
            with st.spinner("Processing your question, please wait"):
                response = conversation_interface(st, user_question)
                st.write(response)
                st.session_state["history"].append({"user_message": user_question, "bot": response})

    with st.sidebar:
        st.write("Uploade PDFs or text docs")
        uploaded_pdfs = st.file_uploader("Upload your PDFs or text docs", type=["pdf", "txt"],
                                         accept_multiple_files=True)
        if not uploaded_pdfs:
            st.error("No files being uploaded")

        if st.button("Upload"):
            with st.spinner("Processing PDFs, please wait"):
                if upload_process_pdfs(uploaded_pdfs):
                    st.success("Files were uploaded successfully, please go ahead and ask any questions")
                else:
                    st.error("An error occurred while processing the files")

    st.write("### Chat History")
    for message in st.session_state["history"]:
        with st.container():
            col1, col2, col3 = st.columns([4, 5, 1])
            with col1:
                st.empty()  # Placeholder to align to the right
            with col2:
                st.markdown(f"**You:** {message['user_message']}")
            with col3:  
                st.image(USER_IMAGE, width=30)

        with st.container():
            col1, col2, col3 = st.columns([1, 8, 1])
            with col1:
                st.image(BOT_IMAGE, width=30)  # Bot image
            with col2:
                st.markdown(f"**Talky:** {message['bot_response']}")
            with col3:
                st.empty()

