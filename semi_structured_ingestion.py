import os
import json

def ingest_semi_structured(semi_dir):
    data = {}

    for file in os.listdir(semi_dir):
        if file.endswith(".json"):
            with open(os.path.join(semi_dir, file), "r", encoding="utf-8") as f:
                data[file] = json.load(f)

    print("✔ Semi-structured data ingested")
    return data
