# 🤖 Help Desk AI Agent (Local RAG)

A local AI-powered help desk agent using:

- FastAPI for backend
- Qdrant for vector similarity search
- Sentence Transformers for local embeddings
- PDF manuals (Mac/Windows/CCNA)

All local — no OpenAI, no cloud, no privacy risk. Runs on your MacBook Pro with M3.

---

## Setup Instructions (Mac)

### 1. Install dependencies

```bash
pip install fastapi uvicorn qdrant-client sentence-transformers langchain pypdf python-dotenv
```

## Start Qdrant Locally
```bash
docker run -p 6333:6333 -p 6334:6334 qdrant/qdrant
```

## Upload another PDF Manual
```bash
python upload_pdf_to_qdrant.py
```

## Start FastAPI Server
```bash
python main.py
```

## Once running, open:

### Swagger UI: 
[SwaggerUi](http://localhost:8080/docs)

### ReDoc: 
[Docs](http://localhost:8080/redoc)

## Creat a ticket/question
```bash
curl -X POST -H "Content-Type: application/json" \
-d '{"ticket":"How do I reset my Mac password?"}' \
http://localhost:8080/request
```

## Get all tickets/respones
```bash
curl -X GET 'http://localhost:8000/requests' -H 'accept: application/json'
```
