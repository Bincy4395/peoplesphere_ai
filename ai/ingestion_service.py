
from pathlib import Path
from uuid import uuid4

from ai.document_loader import load_document
from ai.text_splitter import split_text
from ai.embedding_service import generate_embeddings
from ai.vector_store import store_chunks


# --------------------------------------------------
# 1. Define Document Ingestion Function
# --------------------------------------------------

def ingest_document(
    file_path: str,
    category: str,
    department: str,
    document_id: str | None = None,
    original_file_name: str | None = None
):

    # --------------------------------------------------
    # 1.1 Validate Document
    # --------------------------------------------------

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Document not found: {file_path}"
        )

    # --------------------------------------------------
    # 1.2 Generate or Use Document ID
    # --------------------------------------------------

    if document_id is None:
        document_id = str(uuid4())

    # --------------------------------------------------
    # 1.3 Define Source File Name
    # --------------------------------------------------

    source_name = (
        original_file_name
        if original_file_name
        else path.name
    )

    # --------------------------------------------------
    # 1.4 Load Document
    # --------------------------------------------------

    print("Loading document...")

    content = load_document(str(path))

    if not content.strip():
        raise ValueError(
            "Document contains no extractable text"
        )

    print("Document loaded successfully!")

    # --------------------------------------------------
    # 1.5 Split Text into Chunks
    # --------------------------------------------------

    print("Splitting document...")

    chunks = split_text(content)

    if not chunks:
        raise ValueError(
            "No text chunks generated"
        )

    print(f"Total chunks: {len(chunks)}")

    # --------------------------------------------------
    # 1.6 Generate Embeddings
    # --------------------------------------------------

    print("Generating embeddings...")

    embeddings = generate_embeddings(chunks)

    print("Embeddings generated successfully!")

    # --------------------------------------------------
    # 1.7 Store Chunks in ChromaDB
    # --------------------------------------------------

    print("Storing document in ChromaDB...")

    store_chunks(
        chunks=chunks,
        embeddings=embeddings,
        source=source_name,
        category=category,
        department=department,
        document_id=document_id
    )

    print("Document ingestion completed!")

    # --------------------------------------------------
    # 1.8 Return Ingestion Result
    # --------------------------------------------------

    return {
        "document_id": document_id,
        "source": source_name,
        "total_chunks": len(chunks),
        "status": "success"
    }


# --------------------------------------------------
# 2. Execute and Test Document Ingestion
# --------------------------------------------------

if __name__ == "__main__":

    # --------------------------------------------------
    # 2.1 Define Test Document
    # --------------------------------------------------

    result = ingest_document(
        file_path="documents/uploads/hr_policy.txt",
        category="HR Policy",
        department="HR",
        original_file_name="hr_policy.txt"
    )

    # --------------------------------------------------
    # 2.2 Display Ingestion Result
    # --------------------------------------------------

    print("\nIngestion Result:")
    print(result)
