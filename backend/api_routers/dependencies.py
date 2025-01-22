from fastapi import Request


def get_memory_store(request: Request):
    return request.app.state.memory_store

def get_vector_handler(request: Request):
    return request.app.state.vector_handler

def get_query_handler(request: Request):
    return request.app.state.query_handler