"""Testes dos endpoints de livros."""

LIVRO = {
    "title": "Python Fluente",
    "author": "Luciano Ramalho",
    "published_at": "2015-08-01",
    "summary": "Guia da linguagem Python.",
}

OUTRO_LIVRO = {
    "title": "Arquitetura Limpa",
    "author": "Robert Martin",
    "published_at": "2017-09-10",
    "summary": "Princípios de desenho de software.",
}


def test_cadastra_livro(client):
    response = client.post("/livros", json=LIVRO)

    assert response.status_code == 201
    body = response.json()
    assert body["id"] == 1
    assert body["title"] == LIVRO["title"]
    assert body["author"] == LIVRO["author"]
    assert body["published_at"] == LIVRO["published_at"]
    assert body["summary"] == LIVRO["summary"]


def test_cadastro_sem_titulo_e_rejeitado(client):
    payload = {key: value for key, value in LIVRO.items() if key != "title"}

    response = client.post("/livros", json=payload)

    assert response.status_code == 422


def test_data_invalida_e_rejeitada(client):
    payload = {**LIVRO, "published_at": "31-02-2015"}

    response = client.post("/livros", json=payload)

    assert response.status_code == 422


def test_busca_por_titulo_e_por_autor(client):
    client.post("/livros", json=LIVRO)
    client.post("/livros", json=OUTRO_LIVRO)

    # Trecho do título, em minúsculas: a busca não diferencia maiúsculas.
    por_titulo = client.get("/livros", params={"titulo": "fluente"})
    assert por_titulo.status_code == 200
    assert [livro["title"] for livro in por_titulo.json()] == ["Python Fluente"]

    por_autor = client.get("/livros", params={"autor": "martin"})
    assert por_autor.status_code == 200
    assert [livro["author"] for livro in por_autor.json()] == ["Robert Martin"]


def test_busca_sem_resultado_devolve_lista_vazia(client):
    client.post("/livros", json=LIVRO)

    response = client.get("/livros", params={"titulo": "livro que nao existe"})

    assert response.status_code == 200
    assert response.json() == []


def test_consulta_livro_por_id(client):
    created = client.post("/livros", json=LIVRO).json()

    response = client.get(f"/livros/{created['id']}")

    assert response.status_code == 200
    assert response.json()["title"] == LIVRO["title"]


def test_consulta_id_inexistente(client):
    response = client.get("/livros/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Livro não encontrado"
