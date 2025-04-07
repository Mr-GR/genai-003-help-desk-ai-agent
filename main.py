import os
import uvicorn
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.http.models import Filter, FieldCondition, MatchValue, SearchRequest
from sentence_transformers import SentenceTransformer
import numpy as np

# Load environment variables
load_dotenv()

# Configuration
QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", 6333))
COLLECTION_NAME = "manuals"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
TOP_K = 3

# Initialize app
app = FastAPI(
    title='Help Desk AI (Local RAG + LLM)',
    description='FastAPI Help Desk AI using local sentence-transformers, Qdrant, and Ollama',
    version='1.0.0'
)

# Pydantic models
class RequestTicket(BaseModel):
    ticket: str
    response: str = ""

class AskRequest(BaseModel):
    question: str

class AskResponse(BaseModel):
    answer: str

# In-memory ticket log
ticket_log: List[RequestTicket] = []

# Load local embedding model
model = SentenceTransformer(EMBEDDING_MODEL)

# Connect to Qdrant
qdrant = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)

# Routes
@app.get("/requests")
async def get_requests():
    return ticket_log

@app.post("/request")
async def add_request(ticket: RequestTicket):
    try:
        query_embedding = model.encode(ticket.ticket).tolist()

        search_result = qdrant.search(
            collection_name=COLLECTION_NAME,
            query_vector=query_embedding,
            limit=TOP_K,
            with_payload=True
        )

        response_chunks = [hit.payload["text"] for hit in search_result]
        response = "\n---\n".join(response_chunks)

        new_ticket = RequestTicket(ticket=ticket.ticket, response=response)
        ticket_log.append(new_ticket)
        return new_ticket

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ask", response_model=AskResponse)
async def ask_question(body: AskRequest):
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

# Run server
if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8080, reload=True)
