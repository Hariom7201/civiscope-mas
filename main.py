import os
from dotenv import load_dotenv

from src.embedder import Embedder
from src.qdrant_setup import get_qdrant_client, create_collection_if_not_exists
from src.ingest import ingest_documents
from src.retrieve import retrieve_evidence
from src.recommend import generate_recommendation

def main():
    load_dotenv()

    collection_name = os.getenv("COLLECTION_NAME", "civiscope_memory")

    # 1) Setup Qdrant
    client = get_qdrant_client()

    # 2) Embedding model
    embedder = Embedder()
    test_vec = embedder.encode(["test"])[0]
    vector_size = len(test_vec)

    create_collection_if_not_exists(client, collection_name, vector_size)

    # 3) Sample societal dataset (you can replace later)
    docs = [
        {"source": "news", "text": "Heavy rainfall reported in coastal district. Water level rising near river banks."},
        {"source": "helpline", "text": "Multiple calls about road flooding and blocked drainage in low-lying areas."},
        {"source": "gov_report", "text": "IMD warning: high probability of intense rainfall over next 24 hours."},
        {"source": "social", "text": "People reporting power cuts and water entering houses in some colonies."},
        {"source": "news", "text": "Rescue teams deployed to monitor flood-prone zones."},
    ]

    texts = [d["text"] for d in docs]
    vectors = embedder.encode(texts)

    ingest_documents(client, collection_name, vectors, docs)

    # 4) Query
    query = "flood risk and rising water level alerts"
    query_vec = embedder.encode([query])[0]

    evidence = retrieve_evidence(client, collection_name, query_vec, top_k=4)
    result = generate_recommendation(evidence)

    print("\n=== CIVISCOPE-MAS OUTPUT ===")
    print(f"Query: {query}")
    print(f"Risk Level: {result['risk_level']}")
    print(f"Confidence: {result['confidence']}")
    print("\nEvidence Retrieved:")
    for ev in result["evidence"]:
        print(f"- ({ev['score']}) [{ev['source']}] {ev['text']}")

    print("\nRecommendation:")
    print(result["recommendation"])

if __name__ == "__main__":
    main()
