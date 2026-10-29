"""Testes da busca semântica. Não chamam a API de embeddings."""

from langchain_core.documents import Document

from app.services.search import load_documents, split_documents


def test_load_documents_le_arquivos_txt():
    names = {document.metadata["source"] for document in load_documents()}

    assert "listas.txt" in names
    assert "funcoes.txt" in names
    assert "dicionarios.txt" in names


def test_split_documents_corta_texto_longo():
    document = Document(
        page_content="lista " * 120,
        metadata={"source": "listas.txt"},
    )

    chunks = split_documents([document])

    assert len(chunks) > 1
    assert chunks[0].metadata["source"] == "listas.txt"


def test_busca_devolve_trechos(client, monkeypatch):
    monkeypatch.setattr(
        "app.routers.search.search",
        lambda query: [
            {
                "content": "Uma lista em Python é criada com colchetes.",
                "source": "listas.txt",
                "score": 0.2,
            }
        ],
    )

    response = client.post("/busca", json={"query": "como criar uma lista"})

    assert response.status_code == 200
    body = response.json()["results"]
    assert body[0]["source"] == "listas.txt"
    assert "lista" in body[0]["content"]


def test_busca_sem_texto_e_rejeitada(client):
    response = client.post("/busca", json={"query": ""})

    assert response.status_code == 422


def test_busca_sem_indice_responde_503(client, monkeypatch):
    def missing_index(query):
        raise RuntimeError("Rode python scripts/ingest.py para criar o índice FAISS")

    monkeypatch.setattr("app.routers.search.search", missing_index)

    response = client.post("/busca", json={"query": "lista"})

    assert response.status_code == 503
    assert "ingest.py" in response.json()["detail"]
