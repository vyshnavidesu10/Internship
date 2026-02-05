import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

files = [
    "structured_entities.json",
    "semi_structured_entities.json",
    "unstructured_entities.json"
]

documents = []

for file in files:
    path = os.path.join(BASE_DIR, file)

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

        for item in data:
            # Convert each JSON object into a meaningful sentence
            sentence_parts = []

            for key, value in item.items():
                sentence_parts.append(f"{key.replace('_',' ')}: {value}")

            sentence = " | ".join(sentence_parts)
            documents.append(sentence)

print("✔ Documents created:", len(documents))
print("\nSample:")
for d in documents[:5]:
    print("-", d)
