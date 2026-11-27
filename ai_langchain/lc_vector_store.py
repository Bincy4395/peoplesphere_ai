
from uuid import uuid4

from langchain_chroma import Chroma
from langchain_core.documents import Document

from ai_langchain.lc_embedding import get_embedding_model


# --------------------------------------------------
# 1. Initialize LangChain Chroma
# --------------------------------------------------

embedding_model = get_embedding_model()

vector_store = Chroma(
    collection_name="peoplesphere_lc_documents",
    embedding_function=embedding_model,
    persist_directory="./chroma_db_langchain",
    collection_metadata={"hnsw:space": "cosine"},
)


# --------------------------------------------------
# 2. Store Document Chunks and Embeddings
# --------------------------------------------------

def store_chunks(
    chunks: list[Document],
    source: str,
    category: str,
    department: str,
    document_id: str,
):
    # --------------------------------------------------
    # 2.1 Prepare Chunk IDs and Metadata
    # --------------------------------------------------

    documents = []
    ids = []

    for index, chunk in enumerate(chunks):
        chunk_id = f"{document_id}_chunk_{index}"

        metadata = {
            **chunk.metadata,
            "document_id": document_id,
            "source": source,
            "category": category,
            "department": department,
            "chunk_index": index,
        }

        documents.append(
            Document(
                page_content=chunk.page_content,
                metadata=metadata,
            )
        )

        ids.append(chunk_id)

    # --------------------------------------------------
    # 2.2 Replace Existing Chunks for This Document
    # --------------------------------------------------

    vector_store.delete(
        where={"document_id": document_id}
    )

    # --------------------------------------------------
    # 2.3 Store Documents and Generate Embeddings
    # --------------------------------------------------

    vector_store.add_documents(
        documents=documents,
        ids=ids,
    )

    print(
        f"Successfully stored {len(documents)} chunks "
        f"for document ID: {document_id}"
    )


# --------------------------------------------------
# 3. Delete Document Chunks
# --------------------------------------------------

def delete_document_chunks(document_id: str):
    vector_store.delete(
        where={"document_id": document_id}
    )

    print(
        f"Deleted chunks for document ID: {document_id}"
    )


# --------------------------------------------------
# 4. Retrieve Stored Documents
# --------------------------------------------------

def get_stored_documents():
    results = vector_store.get(
        include=["documents", "metadatas"]
    )

    return results


# --------------------------------------------------
# 5. Test Document Ingestion
# --------------------------------------------------

if __name__ == "__main__":

    from ai_langchain.lc_document_loader import load_document
    from ai_langchain.lc_text_splitter import split_documents

    # --------------------------------------------------
    # 5.1 Define Document Details
    # --------------------------------------------------

    file_path = "documents/lc_uploads/hr_policy.txt"

    category = "HR Policy"
    department = "HR"

    # --------------------------------------------------
    # 5.2 Generate Unique Document ID
    # --------------------------------------------------

    document_id = str(uuid4())

    # --------------------------------------------------
    # 5.3 Load Document
    # --------------------------------------------------

    documents = load_document(file_path)

    # --------------------------------------------------
    # 5.4 Split Document into Chunks
    # --------------------------------------------------

    chunks = split_documents(documents)

    # --------------------------------------------------
    # 5.5 Store Chunks with Metadata
    # --------------------------------------------------

    store_chunks(
        chunks=chunks,
        source=file_path,
        category=category,
        department=department,
        document_id=document_id,
    )

    # --------------------------------------------------
    # 5.6 Verify Stored Documents
    # --------------------------------------------------

    results = get_stored_documents()

    print(
        "\nTotal stored chunks:",
        len(results["ids"]),
    )

    print("\nStored Metadata:")

    for metadata in results["metadatas"]:
        print(metadata)
