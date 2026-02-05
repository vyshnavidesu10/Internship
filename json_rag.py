import faiss
import pickle
from sentence_transformers import SentenceTransformer

index = faiss.read_index("json_documents.index")
model = SentenceTransformer("all-MiniLM-L6-v2")

with open("json_docs.pkl", "rb") as f:
    documents = pickle.load(f)

def json_semantic_search(query, k=5):
    q_emb = model.encode([query]).astype("float32")
    _, indices = index.search(q_emb, k)
    return [documents[i] for i in indices[0]]
