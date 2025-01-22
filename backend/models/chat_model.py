from pydantic import BaseModel
from typing import List, Optional

class LLMResponse(BaseModel):
    response: str
    chat_history: str


class HumanQuestion(BaseModel):
    question: str
    chat_history: Optional[str] = ""