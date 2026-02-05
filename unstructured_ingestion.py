import os
from pypdf import PdfReader

def ingest_unstructured(unstructured_dir):
    texts = {}

    for file in os.listdir(unstructured_dir):
        if file.endswith(".pdf"):
            reader = PdfReader(os.path.join(unstructured_dir, file))
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""
            texts[file] = text

    print("✔ Unstructured data ingested")
    return texts
