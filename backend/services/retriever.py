from services.embeddings import get_embedding
from services.vector_store import get_collection


def retrieve_chunks(query: str, top_k: int = 10):

    collection = get_collection()

    query_embedding = get_embedding(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    # DEBUG OUTPUT
    print("\n===== RAW CHROMA RESULTS =====")

    for i in range(len(results["documents"][0])):

        print("\nRANK:", i + 1)

        print(
            "DISTANCE:",
            results["distances"][0][i]
        )

        print(
            "SOURCE:",
            results["metadatas"][0][i]["source"]
        )

        print("TEXT:")
        print(results["documents"][0][i][:300])

    print("\n============================")

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

    print("\n===== FINAL CHUNKS =====")
    print(chunks)

    return chunks