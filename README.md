# 🤖 Help Desk AI Agent RAG

A local AI-powered help desk agent using:

- **FastAPI** for backend
- **Qdrant** for vector similarity search
- **Sentence Transformers** for local embeddings
- **PDF manuals** (Mac/Windows/CCNA)
- **PostgreSQL** for user authentication
- **Flutter** (mobile/web) UI

---

## Setup Instructions (Mac)

### 1. Install dependencies

```bash
pip install fastapi uvicorn qdrant-client sentence-transformers langchain pypdf python-dotenv sqlalchemy psycopg2-binary passlib[bcrypt] python-jose
```

### 2. Start Qdrant Locally

```bash
docker run -p 6333:6333 -p 6334:6334 qdrant/qdrant
```

### 3. Upload a PDF Manual

```bash
python upload_pdf_to_qdrant.py
```

### 4. Start FastAPI Server

```bash
python main.py
```

---

## Authentication & Token Protection

### Signup

```bash
curl -X POST http://localhost:8080/signup \
  -H "Content-Type: application/json" \
  -d '{"username": "demo", "password": "demo123"}'
```

### Login

```bash
curl -X POST http://localhost:8080/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=demo&password=demo123"
```

### Use Token

```bash
-H "Authorization: Bearer <your_token>"
```

---

## AI-Powered Ticketing

### Create a Ticket (RAG)

```bash
curl -X POST http://localhost:8080/request \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json" \
  -d '{"ticket": "How do I reset my Mac password?"}'
```

### Ask a General Question (LLM)

```bash
curl -X POST http://localhost:8080/ask \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is RAG?"}'
```

### Get All Tickets

```bash
curl -X GET 'http://localhost:8080/requests' \
  -H 'Authorization: Bearer <your_token>'
```

---

## Flutter UI

- **LoginSignUpPage**: Toggle between login & signup
- **HomePage**: Navigation buttons (Chat, Docs, Logout)
- **ChatPage**: Chat with RAG or LLM using token

### Flutter Features

- Auto-login with stored JWT
- Secure API requests using token
- Logout functionality
- Clean & consistent UI design

---

## API Docs

- Swagger UI → [http://localhost:8080/docs](http://localhost:8080/docs)
- Redoc → [http://localhost:8080/redoc](http://localhost:8080/redoc)

---

## Environment Setup

Ensure your `.env` includes:

```env
SECRET_KEY=your_secret
DATABASE_URL=postgresql://user:pass@localhost:5432/helpdesk
```

**Ignore in `.gitignore`:**

```gitignore
.venv/
__pycache__/
.env
```
