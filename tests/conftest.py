"""Banco de teste separado do biblioteca.db.

Cada teste recebe um SQLite em memória, vazio. O arquivo de desenvolvimento
não é aberto e não é alterado.
"""

import os

# Precisa existir antes de importar a aplicação. O lifespan lê esta variável
# e não cria o arquivo biblioteca.db durante os testes.
os.environ["TESTING"] = "1"

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app

# StaticPool faz todas as conexões compartilharem o mesmo banco em memória.
# Sem isso, cada sessão veria um SQLite vazio e diferente.
engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def client():
    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)
