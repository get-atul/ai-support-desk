from dotenv import load_dotenv

from database.connection import init_db
from database.repository import get_project_knowledge_sources
from services.ingestion_service import (
    ingest_text_source,
    index_document,
)


load_dotenv()


print("=" * 60)
print("INITIALIZING DATABASE")
print("=" * 60)

init_db()


print("\n" + "=" * 60)
print("GETTING KNOWLEDGE SOURCE")
print("=" * 60)

project_id = input("Enter Project ID: ").strip()

sources = get_project_knowledge_sources(project_id)

if not sources:
    raise ValueError(
        f"No knowledge sources found for project '{project_id}'."
    )

source = sources[0]

print(f"Source ID: {source.id}")
print(f"Source Name: {source.name}")
print(f"Storage Path: {source.storage_path}")


print("\n" + "=" * 60)
print("INGESTING SOURCE")
print("=" * 60)

document = ingest_text_source(
    source_id=source.id,
)


print("\n" + "=" * 60)
print("DOCUMENT CONTENT")
print("=" * 60)

print(f"Source ID: {document.source_id}")
print(f"Project ID: {document.project_id}")
print(f"Source Name: {document.source_name}")
print(f"Source Type: {document.source_type}")
print(f"Language: {document.language}")

print("\nExtracted Text:")
print(document.text)


print("\n" + "=" * 60)
print("INDEXING DOCUMENT")
print("=" * 60)

print("Starting vector indexing...")

vector_store = index_document(document)
#761c1c60-53cf-4802-b6e5-01dba7b6eda6
print("Vector indexing completed.")
print("\nDocument indexed successfully.")