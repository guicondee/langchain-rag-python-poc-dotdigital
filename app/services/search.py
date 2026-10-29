"""Busca semântica com embeddings da OpenAI e FAISS.

Os textos são cortados em chunks. Cada chunk vira um vetor na API da
OpenAI e o FAISS guarda esses vetores em disco. A consulta usa o mesmo
modelo, para os vetores serem comparáveis.
"""

import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

DOCUMENTS_DIR = Path(__file__).resolve().parents[2] / "data" / "documentos"
INDEX_DIR = Path(__file__).resolve().parents[2] / "data" / "faiss"

# Modelo de embeddings da OpenAI. Não baixa PyTorch na máquina.
EMBEDDING_MODEL = "text-embedding-3-small"
# Os artigos são longos. O corte fica perto de um parágrafo, com sobreposição
# para uma frase no fim de um chunk reaparecer no começo do seguinte.
CHUNK_SIZE = 700
CHUNK_OVERLAP = 80
DEFAULT_LIMIT = 3

_embeddings = None
_store = None


def load_documents() -> list[Document]:
    """Lê os .txt e guarda o nome do arquivo em cada texto."""
    documents = []
    for path in sorted(DOCUMENTS_DIR.glob("*.txt")):
        documents.append(
            Document(
                page_content=path.read_text(encoding="utf-8"),
                metadata={"source": path.name},
            )
        )
    return documents


def split_documents(documents: list[Document]) -> list[Document]:
    """Corta os textos em pedaços com um pouco de sobreposição."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )
    return splitter.split_documents(documents)


def get_embeddings() -> OpenAIEmbeddings:
    """Cria o cliente de embeddings uma vez por processo."""
    global _embeddings
    if _embeddings is None:
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("Defina OPENAI_API_KEY no arquivo .env")
        _embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL, api_key=api_key)
    return _embeddings


def build_index() -> Path:
    """Gera os vetores e grava o índice FAISS em data/faiss."""
    global _store
    chunks = split_documents(load_documents())
    store = FAISS.from_documents(chunks, get_embeddings())
    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    store.save_local(str(INDEX_DIR))
    _store = store
    return INDEX_DIR


def get_store() -> FAISS:
    """Abre o índice salvo. Não recria os embeddings dos documentos."""
    global _store
    if _store is None:
        if not (INDEX_DIR / "index.faiss").exists():
            raise RuntimeError("Rode python scripts/ingest.py para criar o índice FAISS")
        # O arquivo foi gerado pelo nosso ingest, não por um terceiro.
        _store = FAISS.load_local(
            str(INDEX_DIR),
            get_embeddings(),
            allow_dangerous_deserialization=True,
        )
    return _store


def search(query: str, limit: int = DEFAULT_LIMIT) -> list[dict]:
    """Devolve os chunks mais próximos da consulta.

    A pontuação do FAISS aqui é distância: quanto menor, mais parecido.
    """
    found = get_store().similarity_search_with_score(query, k=limit)
    return [
        {
            "content": document.page_content,
            "source": document.metadata.get("source", ""),
            "score": float(score),
        }
        for document, score in found
    ]
