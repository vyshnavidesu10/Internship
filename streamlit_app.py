import streamlit as st
import faiss
from sentence_transformers import SentenceTransformer
from load_documents import documents
from structured_qa import structured_answer
from groq import Groq
import os
import numpy as np
from dotenv import load_dotenv
from pdf_rag import pdf_semantic_search
from json_rag import json_semantic_search

# ---------------- CONFIG ----------------
st.set_page_config(page_title="Enterprise Chatbot", layout="wide")
load_dotenv()

# ---------------- LOAD MODELS ----------------
index = faiss.read_index("documents.index")
model = SentenceTransformer("all-MiniLM-L6-v2")
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ---------------- GLOBAL STYLE ----------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f172a, #020617);
    font-family: 'Segoe UI', sans-serif;
}

.main-title {
    text-align: center;
    font-size: 44px;
    font-weight: 700;
    color: #e5e7eb;
}

.subtitle {
    text-align: center;
    font-size: 16px;
    color: #94a3b8;
    margin-bottom: 30px;
}

.section-title {
    font-size: 20px;
    font-weight: 600;
    color: #60a5fa;
    margin-bottom: 10px;
}

.glass-card {
    background: rgba(255, 255, 255, 0.12);
    backdrop-filter: blur(14px);
    border-radius: 16px;
    padding: 16px;
    margin-bottom: 12px;
    color: #e5e7eb;
    box-shadow: 0 10px 28px rgba(0,0,0,0.35);
}

.badge {
    display: inline-block;
    padding: 6px 14px;
    border-radius: 20px;
    font-size: 13px;
    font-weight: 600;
    background: linear-gradient(90deg, #22c55e, #16a34a);
    color: #022c22;
    margin-bottom: 12px;
}

button {
    background: linear-gradient(90deg, #6366f1, #3b82f6);
    color: white;
    border-radius: 14px;
    height: 3em;
    width: 100%;
    font-size: 16px;
    font-weight: 600;
    border: none;
}

button:hover {
    background: linear-gradient(90deg, #4f46e5, #2563eb);
    transform: scale(1.03);
}

.footer {
    text-align: center;
    color: #94a3b8;
    font-size: 14px;
    margin-top: 45px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("""
<div class="main-title">🤖 Enterprise Chatbot</div>
<div class="subtitle">Ask questions</div>
""", unsafe_allow_html=True)

# ---------------- METRIC + INPUT ROW ----------------
input_col, metric_col = st.columns([3, 1])

with metric_col:
    accuracy_placeholder = st.empty()
    confidence_placeholder = st.empty()

with input_col:
    query = st.text_input(
        "🔍 Enter your question",
        placeholder="e.g. Explain leave policy ?"
    )

# ---------------- METRIC FUNCTIONS ----------------
def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def compute_confidence_score(query, docs):
    q_emb = model.encode(query)
    d_embs = model.encode(docs)
    sims = [cosine_similarity(q_emb, d) for d in d_embs]
    return round(np.mean(sims) * 100, 2)

def compute_accuracy_score(answer, docs):
    ans_emb = model.encode(answer)
    ctx_emb = model.encode(" ".join(docs))
    return round(cosine_similarity(ans_emb, ctx_emb) * 100, 2)

# ---------------- SEARCH HELPERS ----------------
def semantic_search(query, k=5):
    q_embedding = model.encode([query]).astype("float32")
    _, indices = index.search(q_embedding, k)
    return [documents[i] for i in indices[0]]

def is_pdf_question(query):
    keywords = [
        "summary", "summarize", "policy", "annual report",
        "company overview", "engagement", "leave",
        "holiday", "report", "document", "pdf"
    ]
    return any(k in query.lower() for k in keywords)

def is_json_question(query):
    keywords = [
        "email", "ticket", "issue", "meeting",
        "performance", "project", "salary"
    ]
    return any(k in query.lower() for k in keywords)

def llm_answer(question, context):
    prompt = f"""
Answer the question using ONLY the context below.
If the answer is not present, say "Not found in the data".

Context:
{context}

Question:
{question}
"""
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        max_tokens=300
    )
    return response.choices[0].message.content

# ---------------- SEARCH ----------------
if st.button("Search"):
    if not query.strip():
        st.warning("Please enter a question.")
    else:
        structured_result = structured_answer(query)

        if structured_result:
            st.markdown("<div class='glass-card'>🧠 " + structured_result + "</div>", unsafe_allow_html=True)

        else:
            if is_pdf_question(query):
                results = pdf_semantic_search(query)
                source = "📘 PDF Document"
            elif is_json_question(query):
                results = json_semantic_search(query)
                source = "📂 JSON Data"
            else:
                results = semantic_search(query)
                source = "📊 CSV / Structured Data"

            context_text = "\n".join(results)
            answer = llm_answer(query, context_text)

            confidence_score = compute_confidence_score(query, results)
            accuracy_score = compute_accuracy_score(answer, results)

            # 🔥 UPDATE TOP METRICS
            accuracy_placeholder.markdown(
                f"<div class='glass-card'>📊 <b>Accuracy</b><br>{accuracy_score}%</div>",
                unsafe_allow_html=True
            )

            confidence_placeholder.markdown(
                f"<div class='glass-card'>🎯 <b>Confidence</b><br>{confidence_score}%</div>",
                unsafe_allow_html=True
            )

            # 🔥 RESULTS LAYOUT
            col1, col2 = st.columns([1.4, 1])

            with col1:
                st.markdown("<div class='section-title'>📄 Retrieved Context</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='badge'>{source}</div>", unsafe_allow_html=True)
                for r in results:
                    st.markdown(f"<div class='glass-card'>• {r}</div>", unsafe_allow_html=True)

            with col2:
                st.markdown("<div class='section-title'>🧠 Answer</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='glass-card'>{answer}</div>", unsafe_allow_html=True)

# ---------------- FOOTER ----------------
st.markdown("""
<div class="footer">
Enterprise RAG Chatbot
</div>
""", unsafe_allow_html=True)
