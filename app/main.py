"""Sobe a API da biblioteca virtual.

As próximas etapas da prova (chat e busca semântica) entram como novos
routers, incluídos aqui embaixo do router de livros.
"""

import os
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import Base, engine
from app.routers import books, chat

# Importar o módulo registra a tabela Book na metadata do SQLAlchemy.
# Sem isso, create_all não saberia quais tabelas criar.
import app.models  # noqa: F401


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Cria as tabelas no SQLite quando a API sobe.

    Nos testes essa etapa é pulada. O pytest usa um banco em memória,
    separado do arquivo biblioteca.db.
    """
    if os.getenv("TESTING") != "1":
        Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Biblioteca virtual",
    description=(
        "Questão 1: cadastro e consulta de livros. "
        "Questão 2: chat sobre programação em Python."
    ),
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(books.router)
app.include_router(chat.router)
