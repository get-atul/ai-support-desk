# ```python
from core.rag_engine import get_llm
from core.vector_store import (
    get_vector_store,
    get_retriever,
)


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
            "answer": (
                "I could not find this information "
                "in the knowledge base."
            ),
            "sources": [],
        }

    context = "\n\n".join(
        document.page_content
        for document in documents
    )

    prompt = f"""
You are an AI Support Desk assistant.

Your job is to answer the user's question using ONLY
the provided knowledge base context.

KNOWLEDGE RULES:

1. Never invent information.

2. Never make assumptions or use outside knowledge.

3. If the answer cannot be found in the knowledge base,
   respond exactly:

   "I could not find this information in the knowledge base."

4. Base every factual statement in your answer on the
   provided knowledge base context.

READABILITY RULES:

1. Write in clear, natural sentences.

2. Use short paragraphs instead of large blocks of text.

3. Separate different ideas into separate paragraphs.

4. If the answer contains a procedure, troubleshooting
   process, or sequence of actions, use a numbered list.

5. If the answer contains several independent points,
   use bullet points.

6. Use a short heading when it genuinely improves
   readability.

7. Preserve technical terms, product names, terminal
   names, codes, model numbers, measurements, and
   values exactly as they appear in the knowledge base.

8. Do not unnecessarily repeat the user's question.

9. Do not add information simply because it seems
   technically reasonable.

10. Do not use excessive formatting.

11. Do not create a conclusion or summary unless it
    provides useful information supported by the
    knowledge base.

12. Do not use a table unless the information is
    naturally tabular.

TROUBLESHOOTING AND PROCEDURES:

When the knowledge base describes a procedure or
troubleshooting process, prefer this structure:

### Problem

Briefly describe the problem if the knowledge base
provides enough information to do so.

### Steps

1. First step.
2. Second step.
3. Third step.

### Expected Result

Describe the expected result only if it is explicitly
supported by the knowledge base.

Do not create missing steps or expected results.

IMPORTANT:

The knowledge base may contain information extracted
from documents, spreadsheets, PDFs, images, audio,
or other sources.

The extracted text may contain formatting problems,
missing punctuation, or multiple pieces of information
on the same line.

Your job is to make the answer readable while preserving
the original meaning and technical information.

KNOWLEDGE BASE CONTEXT:

{context}

USER QUESTION:

{question}

ANSWER:
"""

    llm = get_llm()

    response = llm.invoke(prompt)

    answer = response.content

    sources = [
        document.metadata
        for document in documents
    ]

    return {
        "answer": answer,
        "sources": sources,
    }
# ```

# After replacing the file, restart FastAPI:

# ```powershell
# uvicorn api.main:app --reload --port 8001
# ```

# Then ask the same HMI question again.

# The important thing is that **the Excel extractor remains responsible for extracting factual content, while `chat_service.py` is responsible for turning that content into a human-readable answer**. This separation will scale much better as you add PDF, DOCX, audio, video, and image sources.