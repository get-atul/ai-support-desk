from core.rag_engine import get_llm
from core.vector_store import get_vector_store, get_retriever


def ask_question(
    project_id: str,
    question: str,
    k: int = 4,
):
    vector_store = get_vector_store()

    retriever = get_retriever(
        vector_store=vector_store,
        project_id=project_id,
        k=k,
    )

    documents = retriever.invoke(question)

    if not documents:
        return {
            "answer": "I could not find relevant information in the knowledge base.",
            "sources": [],
        }

    context = "\n\n".join(
        document.page_content
        for document in documents
    )

    prompt = f"""
You are an AI Support Desk assistant.

Answer the user's question using ONLY the provided knowledge base context.

If the answer is not present in the context, say:
"I could not find this information in the knowledge base."

Do not invent or assume information.

Knowledge Base Context:
{context}

User Question:
{question}

Answer:
"""

    llm = get_llm()

    response = llm.invoke(prompt)

    sources = [
        document.metadata
        for document in documents
    ]

    return {
        "answer": response.content,
        "sources": sources,
    }