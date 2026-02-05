from datetime import datetime
import json
import os

from structured_data_ingestion import ingest_structured
from semi_structured_ingestion import ingest_semi_structured
from unstructured_ingestion import ingest_unstructured
from config import STRUCTURED_DIR, SEMI_DIR, UNSTRUCTURED_DIR


def normalize_records(data_dict, source_type):
    normalized = []
    timestamp = datetime.now().isoformat()

    for i, (file, content) in enumerate(data_dict.items()):
        normalized.append({
            "doc_id": f"{source_type}_{i+1}",
            "timestamp": timestamp,
            "file_name": file,
            "source_type": source_type,
            "data": content.to_dict(orient="records")
                    if hasattr(content, "to_dict")
                    else content
        })

    return normalized




# ---------- INGEST ----------
structured_data = ingest_structured(STRUCTURED_DIR)
semi_structured_data = ingest_semi_structured(SEMI_DIR)
unstructured_data = ingest_unstructured(UNSTRUCTURED_DIR)

# ---------- NORMALIZE ----------
structured_norm = normalize_records(structured_data, "STRUCT")
semi_norm = normalize_records(semi_structured_data, "SEMI")
unstructured_norm = normalize_records(unstructured_data, "UNSTRUCT")

# ---------- SAVE ----------
OUTPUT_DIR = "."

with open(os.path.join(OUTPUT_DIR, "structured_normalized.json"), "w", encoding="utf-8") as f:
    json.dump(structured_norm, f, indent=4)

with open(os.path.join(OUTPUT_DIR, "semi_structured_normalized.json"), "w", encoding="utf-8") as f:
    json.dump(semi_norm, f, indent=4)

with open(os.path.join(OUTPUT_DIR, "unstructured_normalized.json"), "w", encoding="utf-8") as f:
    json.dump(unstructured_norm, f, indent=4)

with open(os.path.join(OUTPUT_DIR, "normalized.json"), "w", encoding="utf-8") as f:
    json.dump(
        {
            "structured": structured_norm,
            "semi_structured": semi_norm,
            "unstructured": unstructured_norm
        },
        f,
        indent=4
    )

print("✔ Normalization completed")
print("✔ Normalized files saved")
