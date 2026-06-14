from fastapi import APIRouter
from pydantic import BaseModel

from services.retriever import retrieve_chunks
from services.generator import generate_answer
from services.general_chat import general_chat

router = APIRouter()


class ChatRequest(BaseModel):
    query: str
    has_document: bool = False
    top_k: int = 3
    rerank_top_n: int = 3
    use_reranker: bool = False


DOCUMENT_KEYWORDS = [
    "resume",
    "cv",
    "document",
    "pdf",
    "file",
    "uploaded",
    "skills",
    "experience",
    "education",
    "project",
    "certification",
    "internship",
    "profile",
    "candidate"
]


@router.post("/chat")
async def chat(request: ChatRequest):

    query_lower = request.query.lower()

    document_related = any(
        keyword in query_lower
        for keyword in DOCUMENT_KEYWORDS
    )

    print("\nHAS DOCUMENT:", request.has_document)
    print("DOCUMENT RELATED:", document_related)

    # ─────────────────────────────────────────────
    # DOCUMENT Q&A PATH
    # ─────────────────────────────────────────────
    if request.has_document and document_related:

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

    # ─────────────────────────────────────────────
    # GENERAL CHAT PATH
    # ─────────────────────────────────────────────
    answer = general_chat(
        request.query
    )

    return {
        "mode": "general",
        "answer": answer,
        "citations": [],
        "chunks": []
    }