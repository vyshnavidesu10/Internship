import faiss
import pickle
from sentence_transformers import SentenceTransformer

# Load FAISS index
pdf_index = faiss.read_index("pdf.index")

# Load documents
with open("pdf_docs.pkl", "rb") as f:
    pdf_docs = pickle.load(f)

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

def pdf_semantic_search(query, k=5):
    q_emb = model.encode([query]).astype("float32")
    _, indices = pdf_index.search(q_emb, k)
    return [pdf_docs[i] for i in indices[0]]
