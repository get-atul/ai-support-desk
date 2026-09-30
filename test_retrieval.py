from dotenv import load_dotenv

from core.vector_store import get_vector_store, get_retriever


load_dotenv()


print("=" * 60)
print("INITIALIZING VECTOR STORE")
print("=" * 60)

vector_store = get_vector_store()


print("\n" + "=" * 60)
print("PROJECT")
print("=" * 60)

project_id = input("Enter Project ID: ").strip()


print("\n" + "=" * 60)
print("QUESTION")
print("=" * 60)

question = input("Enter your question: ").strip()


print("\n" + "=" * 60)
print("SEARCHING KNOWLEDGE BASE")
print("=" * 60)

retriever = get_retriever(
    vector_store=vector_store,
    project_id=project_id,
    k=4,
)

documents = retriever.invoke(question)


print("\n" + "=" * 60)
print("RETRIEVED DOCUMENTS")
print("=" * 60)

print(f"Documents found: {len(documents)}")

for index, document in enumerate(documents, start=1):

    print("\n" + "-" * 60)
    print(f"RESULT {index}")
    print("-" * 60)

    print("Content:")
    print(document.page_content)

    print("\nMetadata:")
    print(document.metadata)