import json
import os
import faiss
import pickle
from sentence_transformers import SentenceTransformer

BASE_DIR = "Semistructure data"   # folder name
FILES = [
    "email_data.json",
    "meeting_data.json",
    "performance.json",
    "project_data.json",
    "salary.json",
    "ticket_data.json"
]

documents = []

for file in FILES:
    path = os.path.join(BASE_DIR, file)
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
        for item in data:
            text = " ".join(str(v) for v in item.values())
            documents.append(f"{text} | source: {file}")

print(f"✔ Loaded {len(documents)} JSON documents")

# ---- Embeddings ----
model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode(documents, show_progress_bar=True).astype("float32")

index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)

faiss.write_index(index, "json_documents.index")

with open("json_docs.pkl", "wb") as f:
    pickle.dump(documents, f)

print("✅ JSON FAISS index built")
