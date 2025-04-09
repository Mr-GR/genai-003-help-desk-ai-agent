from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
import requests
from dependencies import get_current_user, TokenData

router = APIRouter()

class AskRequest(BaseModel):
    question: str

class AskResponse(BaseModel):
    answer: str

@router.post("/ask", response_model=AskResponse)
async def ask_question(body: AskRequest, current_user: TokenData = Depends(get_current_user)):
    try:
        llm_response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",  
                "prompt": body.question,
                "stream": False
            }
        )
        result = llm_response.json()
        return {"answer": result.get("response", "Sorry, no response")}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
