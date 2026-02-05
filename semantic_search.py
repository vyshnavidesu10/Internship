import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from load_documents import documents

index = faiss.read_index("documents.index")
model = SentenceTransformer("all-MiniLM-L6-v2")

def search(query, k=5):
    q_embedding = model.encode([query]).astype("float32")
    distances, indices = index.search(q_embedding, k)

    for i in indices[0]:
        print("-", documents[i])

query = input("Enter query: ")
search(query)
