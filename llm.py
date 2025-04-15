from fastapi import APIRouter, HTTPException, Depends # type: ignore
from pydantic import BaseModel # type: ignore
import requests, os # type: ignore
from sentence_transformers import SentenceTransformer # type: ignore
from qdrant_client import QdrantClient # type: ignore
from qdrant_client.http.models import SearchRequest, PointStruct, Filter # type: ignore
from dependencies import get_current_user, TokenData

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

@router.post("/ask", response_model=AskResponse)
async def ask_question(body: AskRequest, current_user: TokenData = Depends(get_current_user)):
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

        prompt = f"""Only anwser tier one support type questions:
        
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
                    {"role": "system", "content": "Youre a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7,
                "max_tokens": 512
            }
        )

        result = llm_response.json()
        print("[DEBUG] LLM raw response:", llm_response.text)
        return {"answer": result["choices"][0]["message"]["content"]}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
