from fastapi import FastAPI, UploadFile, File
from langserve import add_routes
from api_routers import embedding_service, llm_service, pdf_service
# from backend.pdf_processor import PDFProcessor
from vector_handler import VectorHandler
from netmate import NetMate
from contextlib import asynccontextmanager
from langchain_community.vectorstores import FAISS
import os
import shutil

BASE_LLM_URL = "http://host.docker.internal:11434"


@asynccontextmanager
async def lifespan(app: FastAPI):
    # os.makedirs("information_store/app_default", exist_ok=True)
    vec_obj = VectorHandler()
    llm_obj = NetMate()
    vec_obj.create_default_embeddings()
    app.state.llm_url = BASE_LLM_URL
    app.state.memory_store = {}
    app.state.vector_handler = vec_obj
    app.state.query_handler = llm_obj
    app.state.llm_chain = llm_obj.create_conversational_chain(vec_obj)
    assert app.state.llm_chain is not None
    add_routes(app, app.state.llm_chain)
    yield
    app.state.memory_store.clear()
    vectorstore_path = "vectorstore"
    cleared_index = FAISS()
    cleared_index.save_local(vectorstore_path)
    shutil.rmtree(vectorstore_path)
    print("FAISS index cleared successfully.")



app = FastAPI(
    title="NetMate backend",
    description="API backend for managing LLMs, embeddings, and document queries",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(pdf_service.router, prefix="/pdf", tags=["PDF Management"])
app.include_router(embedding_service.router, prefix="/embeddings", tags=["Vector Embeddings"])
app.include_router(llm_service.router, prefix="/llm", tags=["LLM Chat"])

