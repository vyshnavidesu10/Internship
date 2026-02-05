from pypdf import PdfReader
import os

PDF_DIR = "Unstructured data"

documents = []

for file in os.listdir(PDF_DIR):
    if file.endswith(".pdf"):
        reader = PdfReader(os.path.join(PDF_DIR, file))
        for page in reader.pages:
            text = page.extract_text()
            if text:
                documents.append(text.strip())

print("✔ PDF documents loaded:", len(documents))
