from fastapi import FastAPI, UploadFile, File
from langserve import add_routes
from backend.api_routers import embedding_service, llm_service, pdf_service
# from backend.pdf_processor import PDFProcessor
from backend.vector_handler import VectorHandler
from backend.netmate import NetMate
from contextlib import contextmanager
import os

BASE_LLM_URL = "http://172.18.112.1:11434"


@contextmanager
async def lifespan(app: FastAPI):
    # os.makedirs("information_store/app_default", exist_ok=True)
    vec_obj = VectorHandler()
    llm_obj = NetMate()
    vec_obj.create_default_embeddings()
    app.state.llm_url = BASE_LLM_URL
    app.state.memory_store = {}
    app.state.llm_chain = llm_obj.create_conversational_chain(vec_obj)
    yield
    app.state.memory_store.clear()

app = FastAPI(
    title="NetMate backend",
    description="API backend for managing LLMs, embeddings, and document queries",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(pdf_service.router, prefix="/pdf", tags=["PDF Management"])
app.include_router(embedding_service.router, prefix="embeddings", tags=["Vector Embeddings"])
app.include_router(llm_service.router, prefix="llm", tags=["LLM Chat"])

