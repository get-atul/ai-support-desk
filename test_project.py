from services.source_service import add_source
from database.connection import init_db
from database.repository import (
    create_project,
    get_project,
    get_projects,
    get_project_knowledge_sources,
)


print("=" * 60)
print("INITIALIZING DATABASE")
print("=" * 60)

init_db()

print("Database initialized.")


print("\n" + "=" * 60)
print("CREATING PROJECT")
print("=" * 60)

project = create_project(
    name="AI Support Desk",
    description="AI-powered meeting and knowledge assistant",
)

print(f"Project ID: {project.id}")
print(f"Project Name: {project.name}")


print("\n" + "=" * 60)
# test_file = Path("test_source.txt")

# test_file.write_text(
#     "This is a test knowledge source for the AI Support Desk project.",
#     encoding="utf-8",
# )

# test_file = Path("test_source.txt")

# test_file.write_text(
#     "This is a test knowledge source for the AI Support Desk project.",
#     encoding="utf-8",
# )
# storage = LocalFileStorage()

print("ADDING KNOWLEDGE SOURCES")
print("=" * 60)


source = add_source(
    project_id=project.id,
    file_path="test_source.txt",
    source_type="text",
    mime_type="text/plain",
)

# source2 = create_knowledge_source(
#     project_id=project.id,
#     name="Product Requirements.pdf",
#     source_type="pdf",
# )

# source3 = create_knowledge_source(
#     project_id=project.id,
#     name="Architecture.png",
#     source_type="image",
# )


print(f"Source ID: {source.id}")
print(f"Source Name: {source.name}")
print(f"Source Type: {source.source_type}")
print(f"Storage Path: {source.storage_path}")
print(f"MIME Type: {source.mime_type}")
print(f"File Size: {source.file_size} bytes")
print(f"Status: {source.status}")

# print(
#     f"{source2.name} | "
#     f"{source2.source_type} | "
#     f"{source2.status}"
# )

# print(
#     f"{source3.name} | "
#     f"{source3.source_type} | "
#     f"{source3.status}"
# )


print("\n" + "=" * 60)
print("PROJECT KNOWLEDGE SOURCES")
print("=" * 60)

sources = get_project_knowledge_sources(project.id)

for source in sources:
    print(
        f"{source.id} | "
        f"{source.name} | "
        f"{source.source_type} | "
        f"{source.status}"
    )


print("\n" + "=" * 60)
print("ALL PROJECTS")
print("=" * 60)

projects = get_projects()

for item in projects:
    print(
        f"{item.id} | "
        f"{item.name}"
    )