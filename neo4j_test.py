import json
from neo4j import GraphDatabase

URI = "bolt://localhost:7687"
USER = "neo4j"
PASSWORD = "your_password"

driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))

def load_entities(file):
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)

    with driver.session() as session:
        if isinstance(data, list):
            for e in data:
                session.run(
                    """
                    MERGE (n:Entity {name:$name, type:$type})
                    SET n.source_file = $source
                    """,
                    name=str(e["entity"]),
                    type=e["type"],
                    source=e.get("source_file")
                )
        else:
            for doc in data:
                for e in doc["entities"]:
                    session.run(
                        """
                        MERGE (n:Entity {name:$name, type:$type})
                        SET n.source_file = $source
                        """,
                        name=e["entity"],
                        type=e["type"],
                        source=doc["source_file"]
                    )

load_entities("structured_entities.json")
load_entities("semi_structured_entities.json")
load_entities("unstructured_entities.json")

driver.close()
print("✔ Entities loaded into Neo4j")
