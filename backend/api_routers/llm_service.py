from fastapi import APIRouter, HTTPException, Depends, Request
from backend.models.chat_model import HumanQuestion, LLMResponse
from backend.netmate import NetMate

router = APIRouter()

@router.post("ask-query/")
async def ask_query(human_question: HumanQuestion,
                    request: Request, 
                    netmate: NetMate = Depends()):
    try:
        llm_chain = request.app.state.llm_chain
        response = netmate.query(human_question.question,
                                 human_question.chat_history,
                                 llm_chain)
        return LLMResponse(response=response, chat_history=human_question.chat_history)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
    