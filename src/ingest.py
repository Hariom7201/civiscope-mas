import time
from qdrant_client.models import PointStruct

def ingest_documents(client, collection_name, vectors, payloads):
    points = []
    ts = int(time.time())

    for i, (vec, payload) in enumerate(zip(vectors, payloads)):
        payload["timestamp"] = payload.get("timestamp", ts)
        points.append(PointStruct(id=i + 1, vector=vec, payload=payload))

    client.upsert(collection_name=collection_name, points=points)
