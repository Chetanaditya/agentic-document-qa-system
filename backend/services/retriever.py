from services.embeddings import get_embedding
from services.vector_store import get_collection


def retrieve_chunks(query: str, top_k: int = 5):

    collection = get_collection()

    query_embedding = get_embedding(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    chunks = []

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    distances = results.get("distances", [[]])[0]

    for i in range(len(documents)):

        score = None

        if i < len(distances):
            score = 1 - float(distances[i])

        chunks.append({
            "text": documents[i],
            "source": metadatas[i].get("source"),
            "page": metadatas[i].get("page"),
            "score": score
        })

    print(chunks)

    return chunks