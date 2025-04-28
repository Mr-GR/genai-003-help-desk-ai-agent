from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
import requests, os
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.http.models import SearchRequest, PointStruct, Filter
from dependencies import get_current_user
from db import models, crud
from db.database import get_db
from sqlalchemy.orm import Session
from typing import Optional

router = APIRouter()

EMBEDDING_MODEL = "all-MiniLM-L6-v2"
COLLECTION_NAME = "manuals"
QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", 6333))
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

model = SentenceTransformer(EMBEDDING_MODEL)
qdrant = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)

class AskRequest(BaseModel):
    question: str

class AskResponse(BaseModel):
    answer: str
    suggest_ticket: Optional[bool] = False

def is_it_question(question: str) -> bool:
    it_keywords = [
        "network", "server", "API", "cloud", "Python", "JavaScript",
        "Docker", "Git", "SQL", "debug", "DevOps", "backend", "frontend",
        "VPN", "firewall", "IT support", "ticket", "deployment", "system",
        "infrastructure", "IP address", "proxy", "database", "CI/CD",
        "SSH", "terminal", "command line", "port", "DNS", "IT issue",
        "Mac",
    ]
    return any(keyword.lower() in question.lower() for keyword in it_keywords)

@router.post("/ask", response_model=AskResponse)
async def ask_question(
    body: AskRequest,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not is_it_question(body.question):
        # Save ONLY user message when it's non-IT
        crud.create_chat_message(db, user_id=current_user.id, user_message=body.question)
        return {
            "answer": (
                "This question appears to be outside of IT support.\n\n"
                "Would you like to submit this as a ticket for further review?"
            ),
            "suggest_ticket": True
        }

    try:
        query_embedding = model.encode(body.question).tolist()

        hits = qdrant.search(
            collection_name=COLLECTION_NAME,
            query_vector=query_embedding,
            limit=5,
            with_payload=True
        )

        context_chunks = [hit.payload.get("text", "") for hit in hits]
        combined_context = "\n---\n".join(context_chunks)

        prompt = f"""Only answer tier one IT support type questions:

Context:
{combined_context}

Question: {body.question}"""

        llm_response = requests.post(
            "https://api.together.xyz/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {TOGETHER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "mistralai/Mistral-7B-Instruct-v0.1",
                "messages": [
                    {"role": "system", "content": "You are a helpful IT support assistant."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 512
            }
        )

        result = llm_response.json()
        answer = result["choices"][0]["message"]["content"]

        crud.create_chat_message(
            db,
            user_id=current_user.id,
            user_message=body.question,
            ai_response=answer
        )

        return {"answer": answer}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
