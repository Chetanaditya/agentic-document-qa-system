import uuid
from pathlib import Path

from services.document_loader import load_document
from services.chunker import chunk_documents
from services.embeddings import get_embedding
from services.vector_store import (
    add_chunks,
    get_collection
)


def ingest_document(file_path: str):

    print("\n========== INGESTION START ==========")

    filename = Path(file_path).name

    print("DOCUMENT:", filename)

    # ---------------------------------------
    # STEP 1 : LOAD DOCUMENT
    # ---------------------------------------

    pages = load_document(file_path)

    print("PAGES LOADED:", len(pages))

    # ---------------------------------------
    # STEP 2 : CHUNK DOCUMENT
    # ---------------------------------------

    chunks = chunk_documents(pages)

    print("CHUNKS CREATED:", len(chunks))

    chunk_texts = []
    embeddings = []
    metadatas = []
    ids = []

    # ---------------------------------------
    # STEP 3 : CREATE EMBEDDINGS
    # ---------------------------------------

    for index, chunk in enumerate(chunks):

        text = chunk["text"].strip()

        # Ignore empty chunks
        if not text:
            continue

        chunk_texts.append(text)

        embeddings.append(
            get_embedding(text)
        )

        metadatas.append({
            "source": filename,
            "page": chunk.get("page", 1),
            "chunk_index": index
        })

        ids.append(str(uuid.uuid4()))

    # ---------------------------------------
    # STEP 4 : STORE IN CHROMADB
    # ---------------------------------------

    add_chunks(
        chunk_texts,
        embeddings,
        metadatas,
        ids
    )

    print("EMBEDDINGS STORED:", len(embeddings))

    # ---------------------------------------
    # STEP 5 : DEBUG DATABASE CONTENTS
    # ---------------------------------------

    collection = get_collection()

    results = collection.get(
        include=["documents", "metadatas"]
    )

    print("\n===== ALL CHUNKS IN CHROMADB =====")

    for i in range(len(results["documents"])):

        metadata = results["metadatas"][i]

        print(f"\nCHUNK {i + 1}")

        print(
            "SOURCE:",
            metadata.get("source")
        )

        print(
            "PAGE:",
            metadata.get("page")
        )

        print(
            "CHUNK:",
            metadata.get("chunk_index")
        )

        print(results["documents"][i][:400])

    print("\n==================================")

    print("\n========== INGESTION COMPLETE ==========\n")

    return len(chunk_texts)