import pandas as pd
import re
from datetime import datetime

# Load CSVs
assets = pd.read_csv("Structured data/assets.csv")

# FIX DATE PARSING
assets["purchase_date"] = pd.to_datetime(
    assets["purchase_date"],
    dayfirst=True,
    errors="coerce"
)

def structured_answer(question: str):
    q = question.lower()

    # 1️⃣ Assets under maintenance
    if "under maintenance" in q:
        rows = assets[assets["status"].str.lower() == "under maintenance"]
        if rows.empty:
            return "No assets are under maintenance."

        return "Assets under maintenance:\n" + ", ".join(rows["asset_id"].tolist())

    # 2️⃣ Available laptops
    if "laptop" in q and "available" in q:
        rows = assets[
            (assets["asset_type"].str.lower() == "laptop") &
            (assets["status"].str.lower() == "available")
        ]
        return ", ".join(rows["asset_id"].tolist()) or "No available laptops."

    # 3️⃣ Retired servers
    if "retired" in q and "server" in q:
        rows = assets[
            (assets["asset_type"].str.lower() == "server") &
            (assets["status"].str.lower() == "retired")
        ]
        return ", ".join(rows["asset_id"].tolist()) or "No retired servers."

    # 4️⃣ Purchased after a date
    match = re.search(r"after (\w+ \d{4})", q)
    if match:
        date = pd.to_datetime(match.group(1))
        rows = assets[assets["purchase_date"] > date]
        return ", ".join(rows["asset_id"].tolist())

    return None  # 👈 VERY IMPORTANT
