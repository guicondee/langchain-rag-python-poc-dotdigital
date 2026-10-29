"""Chat sobre Python usando LangChain e a OpenAI.

O system prompt é a regra fixa. A mensagem humana leva um contexto
rotulado e, no final, a pergunta. A cadeia devolve só o texto.
Cada chamada é independente: não há histórico.
"""

import os

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# A prova cita o GPT-4. gpt-4o é o modelo atual dessa família.
MODEL = "gpt-4o"

SYSTEM_PROMPT = """
Você é um assistente de programação em Python integrado a uma API de estudos.
Responda apenas sobre Python.
Use o contexto da mensagem do usuário para decidir o formato da resposta.
Não invente bibliotecas, versões ou comportamento da linguagem.
""".strip()

# O bloco abaixo é o contexto da chamada, no mesmo papel do texto
# que no Node junta os dados conhecidos e a mensagem do cliente.
CONTEXT_TEMPLATE = """
[CONTEXTO DESTA RESPOSTA]
idioma: português
assunto permitido: programação em Python
formato: primeiro a explicação, depois um exemplo curto de código

IMPORTANTE: use este contexto para montar a resposta.
- Explique o conceito em poucas frases, antes do código.
- O exemplo deve ser pequeno e relacionado à pergunta.
- Se a pergunta não for sobre Python, diga que só responde sobre Python e pare.

[PERGUNTA]
{question}
""".strip()


def build_chain():
    """Monta prompt, modelo e parser numa cadeia só."""
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("Defina OPENAI_API_KEY no arquivo .env")

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT),
            ("human", CONTEXT_TEMPLATE),
        ]
    )
    model = ChatOpenAI(
        model=MODEL,
        temperature=0.1,
        api_key=api_key,
    )
    # Devolve só o texto, sem o objeto de mensagem do modelo.
    parser = StrOutputParser()
    return prompt | model | parser


def answer(question: str) -> str:
    """Envia o contexto com a pergunta e devolve o texto da resposta."""
    chain = build_chain()
    return chain.invoke({"question": question})
