from fastapi import Request


def get_memory_store(request: Request):
    return request.app.state.memory_store