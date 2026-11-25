
import chromadb
from uuid import uuid4


# --------------------------------------------------
# 1. Initialize ChromaDB
# --------------------------------------------------

client = chromadb.PersistentClient(
    path="./chroma_db"
)


# --------------------------------------------------
# 2. Create or Get Collection
# --------------------------------------------------

collection = client.get_or_create_collection(
    name="peoplesphere_documents",
    metadata={"hnsw:space": "cosine"}
)


# --------------------------------------------------
# 3. Store Document Chunks and Embeddings
# --------------------------------------------------

def store_chunks(
    chunks: list[str],
    embeddings: list[list[float]],
    source: str,
    category: str,
    department: str,
    document_id: str
):

    # --------------------------------------------------
    # 3.1 Prepare Chunk IDs
    # --------------------------------------------------

    ids = [
        f"{document_id}_chunk_{i}"
        for i in range(len(chunks))
    ]

    # --------------------------------------------------
    # 3.2 Prepare Metadata
    # --------------------------------------------------

    metadatas = [
        {
            "document_id": document_id,
            "source": source,
            "category": category,
            "department": department,
            "chunk_index": i
        }
        for i in range(len(chunks))
    ]

    # --------------------------------------------------
    # 3.3 Store Data in ChromaDB
    # --------------------------------------------------

    collection.upsert(
        ids=ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas
    )

    print(
        f"Successfully stored {len(chunks)} chunks "
        f"for document ID: {document_id}"
    )


# --------------------------------------------------
# 4. Delete Document Chunks
# --------------------------------------------------

def delete_document_chunks(document_id: str):

    # --------------------------------------------------
    # 4.1 Delete Chunks by Document ID
    # --------------------------------------------------

    collection.delete(
        where={
            "document_id": document_id
        }
    )

    print(
        f"Deleted chunks for document ID: {document_id}"
    )


# --------------------------------------------------
# 5. Retrieve Stored Documents
# --------------------------------------------------

def get_stored_documents():

    # --------------------------------------------------
    # 5.1 Get Documents and Metadata
    # --------------------------------------------------

    results = collection.get(
        include=[
            "documents",
            "metadatas"
        ]
    )

    return results


# --------------------------------------------------
# 6. Test Document Ingestion
# --------------------------------------------------

if __name__ == "__main__":

    from ai.document_loader import load_document
    from ai.text_splitter import split_text
    from ai.embedding_service import generate_embeddings

    # --------------------------------------------------
    # 6.1 Define Document Details
    # --------------------------------------------------

    file_path = "documents/uploads/hr_policy.txt"

    category = "HR Policy"
    department = "HR"

    # --------------------------------------------------
    # 6.2 Generate Unique Document ID
    # --------------------------------------------------

    document_id = str(uuid4())

    # --------------------------------------------------
    # 6.3 Load Document
    # --------------------------------------------------

    content = load_document(file_path)

    # --------------------------------------------------
    # 6.4 Split Document into Chunks
    # --------------------------------------------------

    chunks = split_text(content)

    # --------------------------------------------------
    # 6.5 Generate Embeddings
    # --------------------------------------------------

    embeddings = generate_embeddings(chunks)

    # --------------------------------------------------
    # 6.6 Store Chunks with Metadata
    # --------------------------------------------------

    store_chunks(
        chunks=chunks,
        embeddings=embeddings,
        source=file_path,
        category=category,
        department=department,
        document_id=document_id
    )

    # --------------------------------------------------
    # 6.7 Verify Stored Documents
    # --------------------------------------------------

    results = get_stored_documents()

    print(
        "\nTotal stored chunks:",
        len(results["ids"])
    )

    print("\nStored Metadata:")

    for metadata in results["metadatas"]:
        print(metadata)
