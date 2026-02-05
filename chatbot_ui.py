import streamlit as st
import faiss
from sentence_transformers import SentenceTransformer
from load_documents import documents

# ---------------- Load FAISS + Model ----------------
index = faiss.read_index("documents.index")
model = SentenceTransformer("all-MiniLM-L6-v2")

def semantic_search(query, k=5):
    q_embedding = model.encode([query]).astype("float32")
    distances, indices = index.search(q_embedding, k)
    return [documents[i] for i in indices[0]]

# ---------------- UI ----------------
st.set_page_config(
    page_title="Semantic Search & RAG Chatbot",
    layout="centered"
)

st.title("🤖 Semantic Search & RAG Chatbot")
st.write("Ask questions about your dataset using semantic search.")

query = st.text_input("Enter your question:")

if st.button("Search"):
    if not query.strip():
        st.warning("Please enter a question.")
    else:
        results = semantic_search(query)

        st.subheader("📄 Retrieved Context")
        for r in results:
            st.write("•", r)

        st.subheader("🧠 Answer")
        st.write(
            "Based on the retrieved data, the relevant information is shown above."
        )
