import chromadb


client = chromadb.PersistentClient(
    path="chroma_db"
)

collection = client.get_or_create_collection(
    name="rag_documents"
)


def add_chunks(
    chunks,
    embeddings,
    metadatas,
    ids
):

    collection.add(
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids
    )


def get_collection():
    return collection