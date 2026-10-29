"""Rota do chat sobre programação em Python."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.services.chat import answer

router = APIRouter(prefix="/chat", tags=["Chat"])


class ChatQuestion(BaseModel):
    """Pergunta enviada pelo usuário."""

    question: str = Field(
        min_length=1,
        examples=["Como criar uma lista em Python?"],
    )


class ChatAnswer(BaseModel):
    """Resposta do modelo."""

    answer: str


@router.post("", response_model=ChatAnswer)
def answer_question(payload: ChatQuestion):
    """Responde uma pergunta sobre Python. Uma pergunta, uma resposta."""
    try:
        text = answer(payload.question)
    except RuntimeError as error:
        raise HTTPException(status_code=503, detail=str(error)) from error
    return ChatAnswer(answer=text)
