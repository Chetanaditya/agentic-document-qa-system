from sentence_transformers import CrossEncoder

model = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)


def rerank_chunks(
    query,
    chunks,
    top_n=3
):

    pairs = [
        (query, chunk["text"])
        for chunk in chunks
    ]

    scores = model.predict(pairs)

    for chunk, score in zip(chunks, scores):

        chunk["rerank_score"] = float(score)

    chunks.sort(
        key=lambda x: x["rerank_score"],
        reverse=True
    )

    print("\n===== AFTER RERANK =====")

    for i, chunk in enumerate(chunks):

        print(
            f"\nRANK {i+1}"
        )

        print(
            f"RERANK SCORE: "
            f"{chunk['rerank_score']:.4f}"
        )

        print(
            chunk["text"][:300]
        )

    print("\n========================")

    return chunks[:top_n]