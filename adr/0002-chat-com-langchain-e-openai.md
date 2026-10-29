# ADR 0002 — Chat com LangChain e OpenAI

- Status: aceito
- Data: 2026-10-28
- Etapa: 2, chat sobre programação em Python

## Contexto

A prova pede um chat que receba uma pergunta em texto, use LangChain para falar com um LLM da OpenAI e responda sobre programação em Python. O exemplo pedido é a pergunta "Como criar uma lista em Python?". O chat entra no mesmo processo FastAPI da etapa 1. O código continua curto: nomes em inglês, comentários em português.

## Decisão

`POST /chat` chama uma cadeia LangChain. Não é um agent.

- A rota fica em `app/routers/chat.py`. Ela valida o JSON e devolve `{ "question" }` na entrada e `{ "answer" }` na saída.
- A cadeia fica em `app/services/chat.py`, no método `build_chain`. São três passos ligados por pipe: `prompt | model | parser`.
- O prompt tem duas partes. `SYSTEM_PROMPT` é a regra fixa. `CONTEXT_TEMPLATE` é a mensagem humana: idioma, formato da resposta, como usar esse contexto e, no final, a `{question}`.
- O modelo é `gpt-4o`, com `temperature` 0.1. A chave `OPENAI_API_KEY` vem do `.env`, que não entra no git. O `.env.example` só mostra o nome da variável.
- `StrOutputParser` devolve o texto puro. A rota coloca esse texto no campo `answer`.
- Cada request monta a cadeia de novo e manda só a pergunta atual. Não há histórico, checkpointer nem tools.
- Sem a chave, a rota responde 503. Os testes substituem `answer` e não chamam a OpenAI.
- `scripts/example_chat.py` faz a mesma chamada sem subir o Uvicorn.

## Alternativas consideradas

- Chamar o modelo com `SystemMessage` e `HumanMessage` soltos, sem template. Funciona, mas o contexto da pergunta fica espalhado no código em vez de num bloco só.
- `create_agent` com tools, memória e saída estruturada. É o desenho de um bot que consulta sistemas no meio da conversa. Esta questão pede uma pergunta e uma resposta sobre Python.
- Deixar a cadeia dentro da rota. A etapa 1 não tem service porque a rota só grava um livro. Aqui a montagem do prompt é a regra, então ela sai da rota.
- JSON em português (`pergunta`, `resposta`). O mesmo motivo da etapa 1: a URL pode ser `/chat`, os campos do código ficam em inglês.

## Consequências

- Para ver uma resposta de verdade, é preciso uma chave válida e há custo por chamada ao `gpt-4o`.
- O Swagger em `/docs` basta para testar: `POST /chat` com a pergunta de exemplo.
- A resposta muda um pouco entre chamadas, porque o modelo não é determinístico mesmo com temperatura baixa.
- Incluir tools ou memória depois troca esta cadeia por um agent. Até lá, o endpoint continua uma função só.
- A busca semântica da etapa 3 entra como outro router e não usa este chat.
