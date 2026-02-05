import os
import json
import pandas as pd

STRUCTURED_DIR = "Structured data"

entities = []

for file in os.listdir(STRUCTURED_DIR):
    if file.endswith(".csv"):
        file_path = os.path.join(STRUCTURED_DIR, file)

        df = pd.read_csv(file_path)

        # Iterate through rows
        for _, row in df.iterrows():
            for column, value in row.items():

                if pd.notna(value):
                    entities.append({
                        "entity": value,
                        "type": column.upper(),
                        "source_file": file
                    })

# Save entities JSON
with open("structured_entities.json", "w", encoding="utf-8") as f:
    json.dump(entities, f, indent=4)

print("✔ Structured entity extraction completed")
print("✔ structured_entities.json created")
