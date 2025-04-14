import os
from uuid import uuid4
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer
from tqdm import tqdm
import re


PDF_DIR = "Manuals"
PDF_FILES = [f for f in os.listdir(PDF_DIR) if f.endswith(".pdf")]
COLLECTION_NAME = "manuals"
QDRANT_HOST = "localhost"
QDRANT_PORT = 6333
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
BATCH_SIZE = 64 

def fix_encoding_issues(text):
    replacements = {
        'â€¢': '•', 'â€“': '–', 'â€”': '—', 'â€™': '’',
        'â€œ': '“', 'â€�': '”', 'â€‹': '', 'â€': '"',
        'â€˜': '‘', 'â€²': '′', 'â€³': '″',
        'Â': '', 'Ã': '', '¤': '',
    }
    for bad, good in replacements.items():
        text = text.replace(bad, good)

    lines = text.splitlines()
    cleaned_lines = []
    for line in lines:
        line = line.strip()
        lower_line = line.lower()

        if (
            "cisco systems" in lower_line and "all rights reserved" in lower_line
            or re.match(r"^smbuf-\d+$", lower_line)
            or re.match(r"^chapter\s+\d+", lower_line)
        ):
            continue
        cleaned_lines.append(line)


    return "\n".join(cleaned_lines)


print("[INFO] Loading model and Qdrant...")
model = SentenceTransformer(EMBEDDING_MODEL)
qdrant = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)

existing_collections = qdrant.get_collections().collections
collection_names = [col.name for col in existing_collections]

if COLLECTION_NAME not in collection_names:
    print(f"[INFO] Creating collection '{COLLECTION_NAME}'...")
    qdrant.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(
            size=model.get_sentence_embedding_dimension(),
            distance=Distance.COSINE
        )
    )
else:
    print(f"[INFO] Collection '{COLLECTION_NAME}' already exists. Skipping creation.")

for filename in PDF_FILES:
    path = os.path.join(PDF_DIR, filename)
    print(f"[INFO] Processing {filename}...")

    loader = PyPDFLoader(path)
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    chunks = splitter.split_documents(documents)
    print(f"→ {len(documents)} pages → {len(chunks)} chunks")

    all_points = []
    for idx, doc in enumerate(tqdm(chunks, desc="Embedding chunks")):
        text = fix_encoding_issues(doc.page_content)
        embedding = model.encode(text).tolist()

        all_points.append(PointStruct(
            id=str(uuid4()),
            vector=embedding,
            payload={
                "text": text,
                "source": filename
            }
        ))

    print(f"[INFO] Uploading {len(all_points)} chunks in batches of {BATCH_SIZE}...")
    for i in range(0, len(all_points), BATCH_SIZE):
        batch = all_points[i:i + BATCH_SIZE]
        qdrant.upsert(collection_name=COLLECTION_NAME, points=batch)

print("Done uploading all documents!")
