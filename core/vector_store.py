from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

from core.document import DocumentContent


CHROMA_DIR = "vector_db"
COLLECTION_NAME = "knowledge"

EMBEDDING_MODEL = "text-embedding-3-small"


def get_embeddings():
    return OpenAIEmbeddings(
        model=EMBEDDING_MODEL,
    )

def get_vector_store() -> Chroma:
    embeddings = get_embeddings()

    return Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=CHROMA_DIR,
    )


def add_document(
    document: DocumentContent,
) -> Chroma:

    print(
        f"Adding document: "
        f"{document.source_name}"
    )

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
    )

    chunks = splitter.split_text(document.text)

    documents = [
        Document(
            page_content=chunk,
            metadata={
                "project_id": document.project_id,
                "source_id": document.source_id,
                "source_name": document.source_name,
                "source_type": document.source_type,
                "language": document.language or "unknown",
                "chunk_index": index,
            },
        )
        for index, chunk in enumerate(chunks)
    ]

    vector_store = get_vector_store()

    vector_store.add_documents(documents)

    print(
        f"Added {len(documents)} chunks "
        f"to vector store."
    )

    return vector_store


def get_retriever(
    vector_store: Chroma,
    project_id: str,
    k: int = 4,
):
    return vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={
            "k": k,
            "filter": {
                "project_id": project_id,
            },
        },
    )