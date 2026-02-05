import json
import spacy

nlp = spacy.load("en_core_web_sm")

# Load normalized unstructured data
with open("unstructured_normalized.json", "r", encoding="utf-8") as f:
    data = json.load(f)

entities_output = []

for record in data:
    text = record["data"]
    doc = nlp(text)

    entities = []
    for ent in doc.ents:
        entities.append({
            "text": ent.text,
            "label": ent.label_
        })

    entities_output.append({
        "doc_id": record["doc_id"],
        "file_name": record["file_name"],
        "entities": entities
    })

# Save extracted entities
with open("entities.json", "w", encoding="utf-8") as f:
    json.dump(entities_output, f, indent=4)

print("✔ Entity extraction completed")
print("✔ entities.json created")
