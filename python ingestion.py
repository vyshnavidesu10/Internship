import os

BASE_DIR = os.path.abspath("data")

STRUCTURED_DIR = os.path.join(BASE_DIR, "Structured data")
SEMI_DIR = os.path.join(BASE_DIR, "Semistructure data")
UNSTRUCTURED_DIR = os.path.join(BASE_DIR, "Unstructured data")

OUTPUT_DIR = os.path.abspath("outputs")
os.makedirs(OUTPUT_DIR, exist_ok=True)

print(os.listdir(BASE_DIR))
