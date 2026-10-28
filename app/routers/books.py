"""Rotas de cadastro e consulta de livros."""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Book
from app.schemas import BookCreate, BookRead

router = APIRouter(prefix="/livros", tags=["Livros"])


@router.post("", response_model=BookRead, status_code=201)
def create_book(payload: BookCreate, db: Session = Depends(get_db)):
    """Cadastra um livro e devolve o registro com o id."""
    book = Book(
        title=payload.title,
        author=payload.author,
        published_at=payload.published_at,
        summary=payload.summary,
    )
    db.add(book)
    db.commit()
    # Recarrega o objeto para preencher o id gerado pelo SQLite.
    db.refresh(book)
    return book


@router.get("", response_model=list[BookRead])
def list_books(
    titulo: str | None = Query(default=None, description="Parte do título"),
    autor: str | None = Query(default=None, description="Parte do nome do autor"),
    db: Session = Depends(get_db),
):
    """Lista os livros. Os filtros são opcionais e podem ser usados juntos.

    A busca é por trecho e não diferencia maiúsculas de minúsculas.
    Sem filtros, devolve todos os livros.
    """
    query = select(Book)

    # ilike + "%" encontra o texto em qualquer parte do campo.
    if titulo and titulo.strip():
        query = query.where(Book.title.ilike(f"%{titulo.strip()}%"))
    if autor and autor.strip():
        query = query.where(Book.author.ilike(f"%{autor.strip()}%"))

    return db.scalars(query.order_by(Book.id)).all()


@router.get("/{book_id}", response_model=BookRead)
def get_book(book_id: int, db: Session = Depends(get_db)):
    """Consulta um livro pelo id."""
    book = db.get(Book, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    return book
