"""Conexão com o SQLite da biblioteca.

O banco de desenvolvimento é o arquivo biblioteca.db, na raiz do projeto.
Os testes não usam esse arquivo: eles trocam a sessão por um SQLite em memória.
"""

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# O arquivo fica ao lado do código. A prova pede SQLite, que não é um servidor.
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./biblioteca.db")

engine = create_engine(
    DATABASE_URL,
    # O FastAPI pode atender mais de uma requisição ao mesmo tempo.
    # O SQLite, por padrão, recusa isso na mesma conexão. Esta flag libera.
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    """Base dos modelos. O SQLAlchemy usa esta classe para criar as tabelas."""


def get_db():
    """Abre uma sessão por requisição e fecha no fim, mesmo se der erro."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
