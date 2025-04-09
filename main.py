import os
import uvicorn
from fastapi import FastAPI, Header, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from auth import router as auth_router
from rag import router as rag_router
from llm import router as llm_router
from dependencies import get_current_user, TokenData

load_dotenv()

app = FastAPI(
    title='Help Desk AI (Local RAG + LLM)',
    description='FastAPI Help Desk AI using local sentence-transformers, Qdrant, and Ollama',
    version='1.0.0'
)


app.include_router(auth_router)
app.include_router(rag_router)
app.include_router(llm_router)


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
    uvicorn.run("main:app", host="localhost", port=8080, reload=True)
