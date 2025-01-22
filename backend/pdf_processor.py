from PyPDF2 import PdfReader
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
import os


class PDFProcessor:

    def __init__(self, information_dir="information_store"):

        self.file_store=information_dir + "/app_default/"
        self.directory_loader=PyPDFDirectoryLoader(self.file_store)
        self.text_splitter=RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        self.initial_doc_numbers=50


    def load_dir(self):
        docs=self.directory_loader.load()

        '''
        docs = [
            Document(page_content=text, metadata={"source": metadata})
            for text, metadata in raw_docs  # Adjust as needed
        ]
        '''

        return docs


    def store_user_pdf(self):
        pass


    def process_user_pdf(self, document):

        pdf_loader=PdfReader(document)
        text = ""
        for page in pdf_loader.pages:
            text += page.extract_text()
        chunks = self.text_splitter.split_text(text)
        return chunks


    def init_create_chunks(self):

        docs = self.load_dir()
        chunks = self.text_splitter.split_documents(docs[:self.initial_doc_numbers])
        return chunks
