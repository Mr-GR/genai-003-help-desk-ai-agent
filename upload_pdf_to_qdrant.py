import os
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer
from uuid import uuid4


PDF_PATH = "Manuals/MacBookPro.pdf"
COLLECTION_NAME = "manuals"
QDRANT_HOST = "localhost"
QDRANT_PORT = 6333
EMBEDDING_MODEL = "all-MiniLM-L6-v2"  

print("[INFO] Loading and chunking PDF...")
loader = PyPDFLoader(PDF_PATH)
documents = loader.load()

splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
chunks = splitter.split_documents(documents)

print(f"[INFO] Loaded {len(documents)} pages → {len(chunks)} chunks")

print("[INFO] Loading local embedding model...")
model = SentenceTransformer(EMBEDDING_MODEL)

print("[INFO] Connecting to Qdrant...")
qdrant = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)

qdrant.recreate_collection(
    collection_name=COLLECTION_NAME,
    vectors_config=VectorParams(size=model.get_sentence_embedding_dimension(), distance=Distance.COSINE)
)

print("[INFO] Embedding chunks and uploading to Qdrant...")
points = []
for idx, doc in enumerate(chunks):
    text = doc.page_content
    embedding = model.encode(text).tolist()

    points.append(PointStruct(
        id=str(uuid4()),
        vector=embedding,
        payload={
            "text": text,
            "source": os.path.basename(PDF_PATH),
            "chunk": idx
        }
    ))

qdrant.upsert(collection_name=COLLECTION_NAME, points=points)
print(f"[DONE] Uploaded {len(points)} chunks to Qdrant collection '{COLLECTION_NAME}'")
