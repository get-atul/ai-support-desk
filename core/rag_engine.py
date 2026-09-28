#```python
import os

# ============================================================
# OLD MISTRAL IMPORT
# ============================================================
# from langchain_mistralai import ChatMistralAI

# ============================================================
# NEW OPENAI IMPORT
# ============================================================
from langchain_openai import ChatOpenAI

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda

from core.vector_store import (
    build_vector_store,
    load_vector_store,
    get_retriever
)


def get_llm():

    # ========================================================
    # OLD MISTRAL CODE
    # ========================================================
    # return ChatMistralAI(
    #     model="mistral-small-latest",
    #     mistral_api_key=os.getenv("MISTRAL_API_KEY"),
    #     temperature=0.3,
    # )

    # ========================================================
    # NEW OPENAI CODE
    # ========================================================
    return ChatOpenAI(
        model="gpt-5-nano",
        api_key=os.getenv("OPENAI_API_KEY"),
        temperature=0.3,
    )


def format_docs(docs):
    return "\n\n".join(
        [doc.page_content for doc in docs]
    )


def build_rag_chain(transcript: str):

    # Build vector store from the meeting transcript
    vector_store = build_vector_store(transcript)

    # Get retriever
    retriever = get_retriever(
        vector_store,
        k=4
    )

    # Get OpenAI LLM
    llm = get_llm()

    # RAG prompt
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are an expert meeting assistant. Answer the user's question
based ONLY on the meeting transcript context provided below.

If the answer is not found in the context, say:
"I could not find this information in the meeting transcript."

Always be concise and precise. If quoting someone, mention it clearly.

Context from meeting transcript:
{context}""",
            ),
            (
                "human",
                "{question}"
            ),
        ]
    )

    # ========================================================
    # FULL LCEL RAG PIPELINE
    # ========================================================

    rag_chain = (
        {
            "context": retriever | RunnableLambda(format_docs),
            "question": RunnablePassthrough()
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return rag_chain


def load_rag_chain():

    # Load existing vector store
    vector_store = load_vector_store()

    # Get retriever
    retriever = get_retriever()

    # Get OpenAI LLM
    llm = get_llm()

    # RAG prompt
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are an expert meeting assistant. Answer the user's question
based ONLY on the meeting transcript context provided below.

If the answer is not found in the context, say:
"I could not find this information in the meeting transcript."

Always be concise and precise. If quoting someone, mention it clearly.

Context from meeting transcript:
{context}""",
            ),
            (
                "human",
                "{question}"
            ),
        ]
    )

    # ========================================================
    # RAG PIPELINE
    # ========================================================

    rag_chain = (
        {
            "context": retriever | RunnableLambda(format_docs),
            "question": RunnablePassthrough(),
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return rag_chain


def ask_question(rag_chain, question: str) -> str:

    print(f"Question: {question}")

    answer = rag_chain.invoke(question)

    print(f"Answer: {answer}")

    return answer
#```
