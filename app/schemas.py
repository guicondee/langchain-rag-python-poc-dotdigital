"""Formato dos dados que entram e saem da API.

O Pydantic valida o JSON antes de chegar no banco. Campo faltando ou data
inválida vira resposta 422, sem a gente escrever esse tratamento na rota.
"""

from datetime import date

from pydantic import BaseModel, Field


class BookCreate(BaseModel):
    """Corpo do cadastro de um livro."""

    title: str = Field(min_length=1, max_length=200, examples=["Python Fluente"])
    author: str = Field(min_length=1, max_length=200, examples=["Luciano Ramalho"])
    published_at: date = Field(examples=["2026-08-01"])
    summary: str = Field(min_length=1, examples=["Guia da linguagem Python."])


class BookRead(BookCreate):
    """Livro já salvo, com o id gerado pelo banco."""

    id: int

    # Permite montar este schema a partir do objeto Book do SQLAlchemy.
    model_config = {"from_attributes": True}
