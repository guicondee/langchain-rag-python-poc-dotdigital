# langchain-rag-python-poc-dotdigital

Prova de backend com foco em IA. Esta etapa entrega a **Questão 1**: uma API para cadastrar e consultar livros.

O chat (Questão 2) e a busca semântica (Questão 3) entram nas próximas etapas.

## Como rodar

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Se o `python3 -m venv` avisar que o `ensurepip` não está disponível, crie o ambiente sem o pip embutido e instale o pip em seguida:

```bash
python3 -m venv --without-pip .venv
curl -sS https://bootstrap.pypa.io/get-pip.py | .venv/bin/python
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

A API sobe em `http://127.0.0.1:8000`. A documentação interativa fica em `http://127.0.0.1:8000/docs`.

Os livros são gravados no arquivo `biblioteca.db`, na raiz do projeto. Esse arquivo não vai para o git.

## Endpoints

| Método | Caminho | O que faz |
| --- | --- | --- |
| `POST` | `/livros` | Cadastra um livro |
| `GET` | `/livros` | Lista os livros. Filtros opcionais: `titulo` e `autor` |
| `GET` | `/livros/{id}` | Consulta um livro pelo id |

A busca por título e autor encontra um trecho do texto e não diferencia maiúsculas de minúsculas.

Exemplo de cadastro:

```bash
curl -X POST http://127.0.0.1:8000/livros \
  -H "Content-Type: application/json" \
  -d '{"title":"Python Fluente","author":"Luciano Ramalho","published_at":"2015-08-01","summary":"Guia da linguagem Python."}'
```

Consulta:

```bash
curl "http://127.0.0.1:8000/livros?titulo=python"
curl "http://127.0.0.1:8000/livros?autor=ramalho"
curl http://127.0.0.1:8000/livros/1
```

## Testes

```bash
pytest
```

O pytest usa um SQLite em memória, criado e apagado a cada teste. O arquivo `biblioteca.db` de desenvolvimento não entra nos testes.
