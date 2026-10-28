"""Tabela de livros no SQLite."""

from datetime import date

from sqlalchemy import Date, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Book(Base):
    """Um livro da biblioteca virtual.

    Os nomes das colunas ficam em inglês. A API traduz isso nos parâmetros
    de busca (titulo e autor), que aparecem na URL.
    """

    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    author: Mapped[str] = mapped_column(String(200))
    published_at: Mapped[date] = mapped_column(Date)
    summary: Mapped[str] = mapped_column(Text)
