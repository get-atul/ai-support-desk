from fastapi import APIRouter
from pydantic import BaseModel

from services.chat_service import ask_question


router = APIRouter(
    prefix="/projects",
    tags=["Chat"],
)


class ChatRequest(BaseModel):
    question: str


@router.post("/{project_id}/chat")
def chat(
    project_id: str,
    request: ChatRequest,
):
    result = ask_question(
        project_id=project_id,
        question=request.question,
    )

    return result