import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
import openai
from load_documents import documents

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

index = faiss.read_index("documents.index")
model = SentenceTransformer("all-MiniLM-L6-v2")

def retrieve_context(query, k=5):
    q_emb = model.encode([query]).astype("float32")
    _, idx = index.search(q_emb, k)
    return "\n".join([documents[i] for i in idx[0]])

def ask_llm(question):
    context = retrieve_context(question)

    prompt = f"""
Answer the question using the context below.

Context:
{context}

Question:
{question}
"""

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role":"user","content":prompt}],
        temperature=0.3
    )

    print("\n🤖 Answer:")
    print(response.choices[0].message.content)

while True:
    q = input("\nAsk a question (or type exit): ")
    if q.lower() == "exit":
        break
    ask_llm(q)
