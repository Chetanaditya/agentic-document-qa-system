from langchain_text_splitters import RecursiveCharacterTextSplitter


splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)


def chunk_documents(pages):
    chunks = []

    for page in pages:

        page_chunks = splitter.split_text(
            page["text"]
        )

        for chunk in page_chunks:

            chunks.append({
                "text": chunk,
                "page": page["page"]
            })

    return chunks