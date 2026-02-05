import os
import json
import spacy
from pypdf import PdfReader

# Load NLP model
nlp = spacy.load("en_core_web_sm")

UNSTRUCTURED_DIR = "Unstructured data"

entities_output = []

for file in os.listdir(UNSTRUCTURED_DIR):
    if file.endswith(".pdf"):
        file_path = os.path.join(UNSTRUCTURED_DIR, file)

        reader = PdfReader(file_path)
        text = ""

        for page in reader.pages:
            text += page.extract_text() or ""

        doc = nlp(text)

        entities = []
        for ent in doc.ents:
            entities.append({
                "entity": ent.text,
                "type": ent.label_
            })

        entities_output.append({
            "source_file": file,
            "entities": entities
        })

# Save entities
with open("unstructured_entities.json", "w", encoding="utf-8") as f:
    json.dump(entities_output, f, indent=4)

print("✔ Unstructured entity extraction completed")
print("✔ unstructured_entities.json created")
