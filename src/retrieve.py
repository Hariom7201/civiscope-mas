def retrieve_evidence(client, collection_name, query_vector, top_k=5):
    results = client.query_points(
        collection_name=collection_name,
        query=query_vector,
        limit=top_k,
        with_payload=True
    )
    return results.points
