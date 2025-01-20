from pydantic import BaseModel
from typing import List

class LLMResponse(BaseModel):
    response: str
    chat_history: List[str]


class HumanQuestion(BaseModel):
    question: str