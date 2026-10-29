"""Testes do chat. Não chamam a OpenAI."""

import pytest

from app.services.chat import answer


def test_chat_responde_pergunta(client, monkeypatch):
    monkeypatch.setattr(
        "app.routers.chat.answer",
        lambda question: "Uma lista é criada com colchetes: numeros = [1, 2, 3].",
    )

    response = client.post(
        "/chat",
        json={"question": "Como criar uma lista em Python?"},
    )

    assert response.status_code == 200
    assert "lista" in response.json()["answer"]


def test_chat_sem_pergunta_e_rejeitado(client):
    response = client.post("/chat", json={"question": ""})

    assert response.status_code == 422


def test_chat_sem_chave_responde_503(client, monkeypatch):
    def missing_key(question):
        raise RuntimeError("Defina OPENAI_API_KEY no arquivo .env")

    monkeypatch.setattr("app.routers.chat.answer", missing_key)

    response = client.post("/chat", json={"question": "O que é uma lista?"})

    assert response.status_code == 503
    assert response.json()["detail"] == "Defina OPENAI_API_KEY no arquivo .env"


def test_answer_exige_chave(monkeypatch):
    monkeypatch.setattr("app.services.chat.load_dotenv", lambda: None)
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    with pytest.raises(RuntimeError, match="OPENAI_API_KEY"):
        answer("Como criar uma lista em Python?")
