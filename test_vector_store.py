from dotenv import load_dotenv

load_dotenv()
from core.document import DocumentContent
from core.vector_store import (
    add_document,
    get_vector_store,
    get_retriever,
)


print("=" * 60)
print("CREATING TEST DOCUMENT")
print("=" * 60)


document = DocumentContent(
    text="""
    The AI Support Desk project uses FastAPI for the backend.
    The application uses Chroma as the vector database.
    Documents are converted into embeddings before being stored.
    The system supports project-specific knowledge bases.
    """,
    source_id="source-001",
    project_id="project-001",
    source_name="architecture.txt",
    source_type="text",
    language="en",
)


print(f"Project: {document.project_id}")
print(f"Source: {document.source_name}")


print("\n" + "=" * 60)
print("ADDING DOCUMENT TO VECTOR STORE")
print("=" * 60)


vector_store = add_document(document)


print("\n" + "=" * 60)
print("TESTING PROJECT-AWARE RETRIEVER")
print("=" * 60)


retriever = get_retriever(
    vector_store=vector_store,
    project_id="project-001",
    k=3,
)


results = retriever.invoke(
    "Which vector database does the application use?"
)


print("\nRetrieved documents:")

for index, result in enumerate(results, start=1):

    print("\n" + "-" * 40)

    print(f"Result {index}")
    print(f"Content: {result.page_content}")

    print(f"Metadata:")
    print(result.metadata)