from fastapi import APIRouter, HTTPException, Depends # type: ignore
from pydantic import BaseModel # type: ignore
from typing import List
from sentence_transformers import SentenceTransformer # type: ignore
from qdrant_client import QdrantClient # type: ignore
from qdrant_client.http.models import ScoredPoint # type: ignore
import os
from dependencies import get_current_user, TokenData

QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
QDRANT_PORT = int(os.getenv("QDRANT_PORT", 6333))
COLLECTION_NAME = "manuals"
TOP_K = 1 
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

router = APIRouter()
model = SentenceTransformer(EMBEDDING_MODEL)
qdrant = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)

class RequestTicket(BaseModel):
    ticket: str
    response: str = ""

ticket_log: List[RequestTicket] = []

#Multiple return response
# def format_chunks(results: List[ScoredPoint]) -> str:
#     sorted_results = sorted(results, key=lambda r: r.score or 0, reverse=True)
#     return "\n\n---\n\n".join(
#         f"[{r.payload.get('source', 'Manual')}]\n{r.payload.get('text', '').strip()}"
#         for r in sorted_results
#     )

#Single return response
def format_top_chunk(results: List[ScoredPoint]) -> str:
    if not results:
        return "No relevant information found."
    best = max(results, key=lambda r: r.score or 0)
    return f"{best.payload.get('text', '').strip()}\n[{best.payload.get('source', 'Manual')}]"

@router.get("/requests")
async def get_requests():
    return ticket_log

@router.post("/request")
async def add_request(ticket: RequestTicket, current_user: TokenData = Depends(get_current_user)):
    try:
        query_vector = model.encode(ticket.ticket).tolist()
        results = qdrant.search(
            collection_name=COLLECTION_NAME,
            query_vector=query_vector,
            limit=TOP_K,
            with_payload=True,
        )
        response = format_top_chunk(results)
        new_ticket = RequestTicket(ticket=ticket.ticket, response=response)
        ticket_log.append(new_ticket)
        return new_ticket
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
