import json
import os

# 🔹 CHANGE THIS PATH to where your JSON files are on your laptop
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


files = [
    "structured_entities.json",
    "semi_structured_entities.json",
    "unstructured_entities.json"
]

triples = []

for file in files:
    file_path = os.path.join(BASE_DIR, file)

    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        continue

    with open(file_path, "r", encoding="utf-8") as f:
        triples.extend(json.load(f))

print("✔ Total triples loaded:", len(triples))

# Convert triples to sentences (for embeddings / RAG)
documents = []

for t in triples:
    sentence = f"{t.get('entity','')} {t.get('relation','related to')} {t.get('object','')}"
    documents.append(sentence)

# Preview first 50
print("\n🔹 Sample documents:\n")
for doc in documents[:50]:
    print("-", doc)
