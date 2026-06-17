from fastapi import APIRouter
from pydantic import BaseModel

from services.general_chat import general_chat

router = APIRouter()


class ChatRequest(BaseModel):
    query: str


@router.post("/chat")
async def chat(request: ChatRequest):

    print("\n========== GENERAL CHAT ==========")
    print("QUERY:", request.query)

    answer = general_chat(
        request.query
    )

    return {
        "mode": "general",
        "answer": answer,
        "citations": [],
        "chunks": []
    }