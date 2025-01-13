from fastapi import FastAPI, UploadFile, File
from langchain.prompts import ChatPromptTemplate
from langchain_community.chat_models import ChatOllama
from langchain.chains import ConversationalRetrievalChain
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceInstructEmbeddings
from langserve import add_routes
import os
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter


llm = ChatOllama(model="mistral", base_url="http://172.18.112.1:11434")

prompt_template = ChatPromptTemplate.from_messages([
    ("system",
     "You are an expertise in computer networking and internet with immense experience,"\
      "excellent troubleshooter and design expert"),
    ("human",
     "Answer the question based on the following context in "\
      "a most accurate way:\n{context}\n\nQuestion: {question}")
])


