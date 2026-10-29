"""Exemplo da questão 2, sem subir a API.

Rode na raiz do projeto, com o .env preenchido:

    python scripts/example_chat.py
    python scripts/example_chat.py "Como criar um dicionário em Python?"
"""

import sys
from pathlib import Path

# Permite importar o pacote app quando o script é chamado pela raiz.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.services.chat import answer

DEFAULT_QUESTION = "Como criar uma lista em Python?"


def main() -> None:
    question = " ".join(sys.argv[1:]).strip() or DEFAULT_QUESTION
    print(f"Pergunta: {question}\n")
    print(answer(question))


if __name__ == "__main__":
    main()
