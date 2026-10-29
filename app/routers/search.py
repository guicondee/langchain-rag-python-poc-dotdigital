"""Rota da busca semântica."""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.services.search import search

router = APIRouter(prefix="/busca", tags=["Busca"])


class SearchQuery(BaseModel):
    """Texto usado para encontrar os documentos parecidos."""

    query: str = Field(min_length=1, examples=["como criar uma lista"])


class SearchHit(BaseModel):
    """Um trecho encontrado no índice."""

    content: str
    source: str
    score: float


class SearchResponse(BaseModel):
    """Trechos mais próximos da consulta."""

    results: list[SearchHit]


@router.post("", response_model=SearchResponse)
def search_documents(payload: SearchQuery):
    """Busca trechos pelo sentido da consulta, não por palavra exata."""
    try:
        results = search(payload.query)
    except RuntimeError as error:
        raise HTTPException(status_code=503, detail=str(error)) from error
    return SearchResponse(results=results)
