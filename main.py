import os
import uvicorn # type: ignore
from fastapi import FastAPI, Header, HTTPException, Depends # type: ignore
from fastapi.middleware.cors import CORSMiddleware # type: ignore
from dotenv import load_dotenv # type: ignore
from api.auth import router as auth_router
from llm.llm import router as llm_router
from api.transcribe import router as transcribe_router
from api.tickets import router as tickets_router
from api.chat_history import router as chat_history_router
from api.user import router as user_router
from api.dependencies import get_current_user
from db.schemas import TokenData

load_dotenv()

app = FastAPI(
    title='Help Desk AI (Local RAG + LLM)',
    description='FastAPI Help Desk AI using togther.ai and Qdrant',
    version='1.0.0'
)


app.include_router(auth_router)
app.include_router(llm_router)
app.include_router(transcribe_router)
app.include_router(tickets_router)
app.include_router(chat_history_router)
app.include_router(user_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/protected-chat")
def protected_chat(current_user: TokenData = Depends(get_current_user)):
    return {
        "message": f"🔐 Secure content for {current_user.username}",
        "status": "success"
    }
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
