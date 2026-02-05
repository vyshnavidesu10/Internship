import os
import json

SEMI_DIR = "Semistructure data"

entities = []

for file in os.listdir(SEMI_DIR):
    if file.endswith(".json"):
        with open(os.path.join(SEMI_DIR, file), "r", encoding="utf-8") as f:
            data = json.load(f)

        # Case 1: JSON is a list of records
        if isinstance(data, list):
            records = data
        else:
            # Case 2: JSON is a single object
            records = [data]

        for record in records:
            for key, value in record.items():

                # Simple scalar entities
                if isinstance(value, (str, int, float)):
                    entities.append({
                        "entity": value,
                        "type": key.upper(),
                        "source_file": file
                    })

                # Nested objects (metadata, details, etc.)
                elif isinstance(value, dict):
                    for k, v in value.items():
                        if isinstance(v, (str, int, float)):
                            entities.append({
                                "entity": v,
                                "type": k.upper(),
                                "source_file": file
                            })

# Remove empty entities
entities = [e for e in entities if e["entity"] not in ["", None]]

with open("semi_structured_entities.json", "w", encoding="utf-8") as f:
    json.dump(entities, f, indent=4)

print("✔ Semi-structured entity extraction completed")
print("✔ semi_structured_entities.json created")
