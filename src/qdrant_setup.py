import os
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance

def get_qdrant_client():
    url = os.getenv("QDRANT_URL", "http://localhost:6333")
    api_key = os.getenv("QDRANT_API_KEY", None) or None
    return QdrantClient(url=url, api_key=api_key)

def create_collection_if_not_exists(client, collection_name: str, vector_size: int):
    collections = client.get_collections().collections
    names = [c.name for c in collections]

    if collection_name not in names:
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
        )

