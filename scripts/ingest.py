"""Monta o índice FAISS uma vez.

Rode na raiz do projeto, antes de consultar a API:

    python scripts/ingest.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.services.search import build_index


def main() -> None:
    index_dir = build_index()
    print(f"Índice salvo em {index_dir}")


if __name__ == "__main__":
    main()
