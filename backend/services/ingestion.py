import uuid
from pathlib import Path

from services.document_loader import load_document
from services.chunker import chunk_documents
from services.embeddings import get_embedding
from services.vector_store import add_chunks, get_collection


def ingest_document(file_path: str):

    pages = load_document(file_path)

    chunks = chunk_documents(pages)

    filename = Path(file_path).name

    chunk_texts = []
    embeddings = []
    metadatas = []
    ids = []

    for chunk in chunks:

        chunk_texts.append(
            chunk["text"]
        )

        embeddings.append(
            get_embedding(chunk["text"])
        )

        metadatas.append({
            "source": filename,
            "page": chunk["page"]
        })

        ids.append(
            str(uuid.uuid4())
        )

    # Store chunks in ChromaDB
    add_chunks(
        chunk_texts,
        embeddings,
        metadatas,
        ids
    )

    # ====================================
    # DEBUG: Show everything stored in DB
    # ====================================

    collection = get_collection()

    results = collection.get()

    print("\n===== ALL CHUNKS IN CHROMADB =====")

    for i, doc in enumerate(results["documents"]):

        print(f"\nCHUNK {i + 1}")
        print(doc[:500])

    print("\n==================================")

    return len(chunks)