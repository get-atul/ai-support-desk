from database.connection import init_db
from database.repository import get_knowledge_source


init_db()

source_id = input("Enter Source ID: ").strip()

source = get_knowledge_source(source_id)

if source is None:
    print("Source not found.")
else:
    print("\nSource found:")
    print(f"ID: {source.id}")
    print(f"Project ID: {source.project_id}")
    print(f"Name: {source.name}")
    print(f"Type: {source.source_type}")
    print(f"Storage Path: {source.storage_path}")
    print(f"MIME Type: {source.mime_type}")
    print(f"Status: {source.status}")