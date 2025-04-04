import os
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.http.models import Filter, FieldCondition, MatchValue, SearchRequest
from sentence_transformers import SentenceTransformer
import numpy as np

# Load .env (optional, in case you want host/port as env vars)
load_dotenv()

QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", 6333))
COLLECTION_NAME = "manuals"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
TOP_K = 3 


app = FastAPI(
    title='Help Desk AI (Local RAG)',
    description='FastAPI powered Help Desk AI using local sentence-transformers and Qdrant',
    version='0.2.0'
)

class Request(BaseModel):
    ticket: str
    response: str = ""

requests: List[Request] = []

model = SentenceTransformer(EMBEDDING_MODEL)
qdrant = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)

@app.get("/requests")
async def get_requests():
    return requests

@app.post("/request")
async def add_request(ticket: Request):
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

        new_ticket = Request(ticket=ticket.ticket, response=response)
        requests.append(new_ticket)
        return new_ticket

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8080, reload=True)
