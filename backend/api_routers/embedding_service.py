from vector_handler import VectorHandler
from fastapi import APIRouter, HTTPException, Depends
from api_routers.dependencies import get_memory_store, get_vector_handler

router = APIRouter()


@router.post("/create-user-embeddings/")
async def create_user_embeddings(file_name:str,
                                 memory_store: dict = Depends(get_memory_store),
                                 vec_obj: VectorHandler = Depends(get_vector_handler)):
    try:
        print(memory_store.keys())
        chunks = memory_store.get(file_name)
        if not chunks:
            raise HTTPException(status_code=404, detail="File not found in memory store")
        vec_obj.create_adhoc_embeddings(chunks, file_name)
        del memory_store[file_name]

        return {"message": f"User embeddings created for {file_name}"}
    except Exception as e:
        return {"error": f"An error occurred: {e}"}