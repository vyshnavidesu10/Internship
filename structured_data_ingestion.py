import os
import pandas as pd

def ingest_structured(structured_dir):
    dfs = {}

    for file in os.listdir(structured_dir):
        if file.endswith(".csv"):
            path = os.path.join(structured_dir, file)
            dfs[file] = pd.read_csv(path)

    print("✔ Structured data ingested")
    return dfs
