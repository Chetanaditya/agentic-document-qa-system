from fastapi import APIRouter
from pydantic import BaseModel

from services.retriever import retrieve_chunks
from services.generator import generate_answer

router = APIRouter()


class DocumentChatRequest(BaseModel):
    query: str
    top_k: int = 3
    rerank_top_n: int = 3
    use_reranker: bool = False


@router.post("/document-chat")
async def document_chat(request: DocumentChatRequest):

    chunks = retrieve_chunks(
        request.query,
        request.top_k
    )

    answer = generate_answer(
        request.query,
        chunks
    )

    citations = []

    for chunk in chunks:
        citations.append({
            "source": chunk["source"],
            "page": chunk["page"],
            "text": chunk["text"]
        })

    return {
        "mode": "document",
        "answer": answer,
        "citations": citations,
        "chunks": chunks
    }