import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from load_documents import documents
from load_pdf_documents import documents


model = SentenceTransformer("all-MiniLM-L6-v2")

embeddings = model.encode(documents, show_progress_bar=True)
embeddings = np.array(embeddings).astype("float32")

index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)

faiss.write_index(index, "documents.index")
np.save("documents.npy", embeddings)

print("✔ FAISS index built")
