import os
import faiss
import pickle
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
from langchain_text_splitters import RecursiveCharacterTextSplitter
# -------- CONFIG --------
PDF_DIR = "Unstructured data"   # folder name exactly as in your project
INDEX_FILE = "pdf.index"
DOC_FILE = "pdf_docs.pkl"

# -------- LOAD PDFs --------
documents = []

for file in os.listdir(PDF_DIR):
    if file.endswith(".pdf"):
        reader = PdfReader(os.path.join(PDF_DIR, file))
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""

        documents.append({"text": text, "source": file})

print(f"✔ Loaded {len(documents)} PDFs")

# -------- SPLIT TEXT --------
splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

chunks = []
for doc in documents:
    for chunk in splitter.split_text(doc["text"]):
        chunks.append(f"{chunk}\nSOURCE: {doc['source']}")

print(f"✔ Created {len(chunks)} text chunks")

# -------- EMBEDDINGS --------
model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode(chunks, show_progress_bar=True)

# -------- FAISS --------
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

faiss.write_index(index, INDEX_FILE)

with open(DOC_FILE, "wb") as f:
    pickle.dump(chunks, f)

print("✅ PDF FAISS index built successfully")
