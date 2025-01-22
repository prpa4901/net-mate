from pdf_processor import PDFProcessor
from fastapi import APIRouter, HTTPException, File, UploadFile, Depends
from api_routers.dependencies import get_memory_store

router = APIRouter()


@router.post("/upload/")
async def upload_pdf(file: UploadFile = File(...),
                     memory_store: dict = Depends(get_memory_store),
                     pdf_processor_obj: PDFProcessor = Depends()):
    try:
        chunks = pdf_processor_obj.process_user_pdf(file.file)
        memory_store[file.filename] = chunks
        return {"message": "Uploaded and processed the file {file.filename} successfully"}
    except Exception as e:
        return {"error": f"An error occurred: {e}"}








