# ADR 0001 — API de livros com FastAPI e SQLite

- Status: aceito
- Data: 2026-10-28
- Etapa: 1, cadastro e consulta de livros

## Contexto

A prova pede uma API para cadastrar e consultar livros, com SQLite, endpoints documentados e testes. O framework pode ser Django, Flask ou FastAPI. As etapas seguintes entram no mesmo projeto: um chat com LangChain e uma busca semântica. O código precisa continuar curto e legível.

## Decisão

A etapa 1 é uma API FastAPI síncrona, com SQLAlchemy 2 e SQLite em arquivo.

- A aplicação sobe com Uvicorn (`uvicorn app.main:app`). A porta 8000 é a padrão do servidor, não uma configuração do código.
- O banco de desenvolvimento é o arquivo `biblioteca.db` na raiz. Não há servidor de banco e não há Docker.
- As tabelas são criadas no startup com `Base.metadata.create_all`. Não há ferramenta de migration nesta etapa.
- Cada requisição recebe uma sessão pelo `Depends(get_db)` e a sessão fecha no fim da requisição.
- O contrato HTTP fica no Pydantic (`schemas.py`). A tabela fica no model SQLAlchemy (`models.py`). A rota em `routers/books.py` liga os dois. Não há camada de service nem de repository.
- A URL fica em português: `/livros`, com filtros `titulo` e `autor`. Os campos do JSON e as colunas ficam em inglês: `title`, `author`, `published_at`, `summary`.
- Os testes usam outro SQLite, em memória. Com `TESTING=1`, o startup não cria nem altera o `biblioteca.db`.

Endpoints desta etapa:

- `POST /livros`
- `GET /livros`
- `GET /livros/{book_id}`

## Alternativas consideradas

- Django REST Framework ou Flask. Atendem a prova, mas o chat e a busca semântica ficariam em outro estilo. FastAPI deixa as três etapas no mesmo processo.
- Postgres ou outro banco em container. O enunciado pede SQLite, que é um arquivo. Docker não separa nada nesta etapa.
- SQLModel. É mais curto em alguns exemplos, mas SQLAlchemy é o que se espera ver numa prova de backend.
- Service e repository desde o primeiro endpoint. Com três rotas, essa separação só aumenta o número de arquivos.
- Alias do Pydantic para o JSON sair em português (`titulo`, `autor`). Deixa a URL e o Swagger alinhados, mas espalha tradução pelo código. Foi descartado.
- Alembic para migrations. Faz sentido quando o schema passa a mudar com o tempo. Aqui a tabela nasce vazia no startup.

## Consequências

- Qualquer pessoa sobe a API com um virtualenv e o Uvicorn. Não precisa de Docker nem de um banco instalado como serviço.
- O `biblioteca.db` não entra no git. Apagar o arquivo e subir de novo recria a tabela vazia.
- `create_all` não altera uma tabela que já existe. Uma mudança de coluna no model não migra o arquivo antigo sozinha.
- A rota fala direto com o banco. Se a regra de negócio crescer, o lugar natural de extraí-la é um service, não agora.
- Os testes não dependem do arquivo de desenvolvimento, porque trocam a sessão por um banco em memória.
- Chat e busca semântica entram depois como novos routers no mesmo `app`, sem mudar esta decisão.
