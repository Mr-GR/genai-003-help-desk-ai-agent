from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
import os
import numpy as np
from dependencies import get_current_user, TokenData

router = APIRouter()
QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", 6333))
COLLECTION_NAME = "manuals"
TOP_K = 3

model = SentenceTransformer("all-MiniLM-L6-v2")
qdrant = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)

class RequestTicket(BaseModel):
    ticket: str
    response: str = ""

ticket_log: List[RequestTicket] = []

@router.get("/requests")
async def get_requests():
    return ticket_log

@router.post("/request")
async def add_request(ticket: RequestTicket, current_user : TokenData = Depends(get_current_user)):
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
