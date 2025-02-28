from pydantic import BaseModel, Field
# from typing import List, Optional, Literal, Union
# from langchain_core.messages import HumanMessage, AIMessage

class HumanQuestion(BaseModel):
    question: str

class LLMResponse(BaseModel):
    response: str

