from core.storage import LocalFileStorage


storage = LocalFileStorage()


project_id = "project-001"
source_id = "source-001"


print("=" * 60)
print("SAVING FILE")
print("=" * 60)


stored_path = storage.save(
    project_id=project_id,
    source_id=source_id,
    file_path="test_source.txt",
)


print(f"Stored file: {stored_path}")


print("\n" + "=" * 60)
print("READING FILE")
print("=" * 60)


file_path = storage.get(
    project_id=project_id,
    source_id=source_id,
    file_name="test_source.txt",
)


print(f"Retrieved file: {file_path}")
print(f"Exists: {file_path.exists()}")