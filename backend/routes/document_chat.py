from fastapi import APIRouter
from pydantic import BaseModel


from services.agent import agentic_answer

router = APIRouter()


class DocumentChatRequest(BaseModel):
    query: str
    top_k: int = 3
    rerank_top_n: int = 3
    use_reranker: bool = False


@router.post("/document-chat")
async def document_chat(request: DocumentChatRequest):

    result = agentic_answer(
        request.query,
        request.top_k
    )

    return {
        "mode": "document",
        "answer": result["answer"],
        "citations": result["citations"],
        "chunks": result["chunks"]
    }