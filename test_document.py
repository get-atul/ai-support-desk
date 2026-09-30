from core.document import DocumentContent


document = DocumentContent(
    text="This is a test document.",
    source_id="source-001",
    project_id="project-001",
    source_name="test.txt",
    source_type="text",
    language="en",
)


print("=" * 60)
print("DOCUMENT CONTENT")
print("=" * 60)

print(f"Text: {document.text}")
print(f"Source ID: {document.source_id}")
print(f"Project ID: {document.project_id}")
print(f"Source Name: {document.source_name}")
print(f"Source Type: {document.source_type}")
print(f"Language: {document.language}")
print(f"Metadata: {document.metadata}")