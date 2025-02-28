from langchain_community.embeddings import HuggingFaceInstructEmbeddings
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import FAISS
# import torch
import os
from pdf_processor import PDFProcessor


class VectorHandler:

    def __init__(self, vectorstore_dir="/backend/vectorstore",
                 model_name="hkunlp/instructor-large"):

        # model_device = "cuda" if torch.cuda.is_available() else "cpu"
        model_device = "cpu"

        print(f"Model will run on: {model_device}")

        self.embeddings = HuggingFaceInstructEmbeddings(model_name=model_name,
                                                        model_kwargs={"device":model_device},
                                                        encode_kwargs={"normalize_embeddings":True})
        # self.file_store=upload_dir
        self.vector_dir=vectorstore_dir
        # self.pdf_obj = PDFProcessor()
        os.makedirs(os.path.dirname(self.vector_dir), exist_ok=True)
        self.vector_store=self.load_vector_store()


    def load_vector_store(self):

        """Load an existing vector store or initialize a new one."""

        if os.path.exists(self.vector_dir) and (
            os.path.exists(os.path.join(self.vector_dir, "index.faiss"))
            and os.path.exists(os.path.join(self.vector_dir, "index.pkl"))
        ):
            return FAISS.load_local(self.vector_dir,
                                    self.embeddings,
                                    allow_dangerous_deserialization=True)
        else:
            return FAISS


    def create_default_embeddings(self, force_recreate=False):

        """Generate embeddings for the given documents and save to vectorstore."""

        if not force_recreate and hasattr(self.vector_store, "index") and self.vector_store.index is not None:
            if hasattr(self.vector_store.index, "ntotal") and self.vector_store.index.ntotal > 0:
                print(f"Vector store already exists at {self.vector_dir}. Skipping creation.")
                return
        pdf_obj = PDFProcessor()
        init_chunks = pdf_obj.init_create_chunks()
        self.vector_store = FAISS.from_documents(init_chunks, self.embeddings)
        self.vector_store.save_local(self.vector_dir)
        # return init_vectors


    def create_adhoc_embeddings(self, chunks, uploaded_doc):

        """
        Add embeddings for an ad-hoc user-uploaded document.
        
        Args:
            uploaded_file: The uploaded file object from the user.
        """

        file_name = getattr(uploaded_doc, "name", None) \
          or getattr(uploaded_doc, "filename", "uploaded_document.pdf")

        # chunks = self.pdf_obj.load_user_pdf(uploaded_doc)
        user_chunks = [{"text": chunk, "metadata": {"source": file_name}} for chunk in chunks]
        self.vector_store.add_texts(
            texts=[chunk["text"] for chunk in user_chunks],
            metadatas=[chunk["metadata"] for chunk in user_chunks],
            embeddings=self.embeddings,
        )
        self.vector_store.save_local(self.vector_dir)

