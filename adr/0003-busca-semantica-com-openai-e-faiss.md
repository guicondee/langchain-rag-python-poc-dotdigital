# ADR 0003 — Busca semântica com embeddings da OpenAI e FAISS

- Status: aceito
- Data: 2026-10-29
- Etapa: 3, busca semântica de documentos

## Contexto

A prova pede um conjunto de textos, embeddings gerados por um modelo, o armazenamento desses vetores em FAISS ou Milvus, e uma busca que devolva os trechos mais próximos de uma consulta. A dica cita bibliotecas como transformers. O chat da etapa 2 já usa a OpenAI pela variável `OPENAI_API_KEY`. O índice entra no mesmo processo FastAPI.

## Decisão

A busca usa embeddings da OpenAI e um índice FAISS em disco.

- Os artigos ficam em `data/documentos/` (`listas.txt`, `funcoes.txt`, `dicionarios.txt`).
- `scripts/ingest.py` chama `build_index` em `app/services/search.py`. O texto é cortado com `RecursiveCharacterTextSplitter` (700 caracteres, sobreposição de 80). Cada chunk vira um vetor com `text-embedding-3-small`. O FAISS grava o índice em `data/faiss/`, que não entra no git.
- `POST /busca` só abre esse índice. A consulta é embedada com o mesmo modelo e a resposta traz `content`, `source` e `score`. O `score` é distância: quanto menor, mais parecido.
- A chave é a mesma do chat, `OPENAI_API_KEY` no `.env`. Sem a chave, o ingest para. Sem o índice, a rota responde 503 e pede para rodar o ingest.
- Os testes leem os arquivos, conferem o corte e substituem a busca. Não chamam a OpenAI.

## Alternativas consideradas

- `sentence-transformers` na máquina, como a dica sugere. O pacote puxa o PyTorch com as bibliotecas CUDA e o download passou de alguns gigabytes, a ponto de travar o computador. O enunciado pede um modelo de embeddings, não um modelo local.
- Milvus. É um servidor à parte. O FAISS é um arquivo, no mesmo espírito do SQLite da etapa 1, e não precisa de Docker.
- Embutir a busca no chat. A prova pede uma função de busca. O endpoint fica separado, em `/busca`.

## Consequências

- O ingest e a consulta gastam a cota da mesma chave. Sem uma chave válida, o índice não é criado e `/busca` responde 503.
- Trocar o modelo de embedding exige rodar o ingest de novo. Vetores de modelos diferentes não se comparam.
- O índice é gerado por este projeto. A leitura usa `allow_dangerous_deserialization=True` porque o formato do FAISS no LangChain passa por pickle.
- Apagar `data/faiss/` e rodar o ingest de novo reconstrói o índice a partir dos `.txt`.
