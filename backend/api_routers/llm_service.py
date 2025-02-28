from fastapi import APIRouter, HTTPException, Depends, Request
from models.chat_model import HumanQuestion, LLMResponse, HumanMessage, AIMessage
from api_routers.dependencies import get_query_handler
from netmate import NetMate

router = APIRouter()

@router.post("/ask-query/")
async def ask_query(human_question: HumanQuestion,
                    request: Request,
                    netmate: NetMate = Depends(get_query_handler)):
    try:
        llm_chain = request.app.state.llm_chain
        chat_history = request.app.state.chat_history

        response = netmate.query(human_question.question,
                                 chat_history,
                                 llm_chain)
        # print(response)
        chat_history.append(HumanMessage(content=human_question.question))
        chat_history.append(AIMessage(content=response['answer']))
        '''
        updated_chat_history = (
            f"{chat_history}\nUser: {human_question.question}\nBot: {response['answer']}" if chat_history
            else f"User: {human_question.question}\nBot: {response['answer']}"
        )
        '''
        return LLMResponse(response=str(response['answer']))
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=f"Invalid input: {ve}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")
    