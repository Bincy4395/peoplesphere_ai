
from ollama import embed

from ai.vector_store import collection


# --------------------------------------------------
# 1. Search relevant documents
# --------------------------------------------------
def search_documents(
    query: str,
    top_k: int = 3,
    distance_threshold: float = 0.7
):
    # --------------------------------------------------
    # 2. Generate embedding for user question
    # --------------------------------------------------
    response = embed(
        model="nomic-embed-text",
        input=query
    )

    query_embedding = response["embeddings"][0]

    # --------------------------------------------------
    # 3. Search similar vectors in ChromaDB
    # --------------------------------------------------
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "metadatas", "distances"]
    )

    # --------------------------------------------------
    # Debug: Check Retrieved Documents and Distances
    # --------------------------------------------------
    print("\nQuestion:", query)

    print("\nRetrieved Distances:")
    print(results["distances"][0])

    print("\nRetrieved Documents:")
    for document, distance in zip(
        results["documents"][0],
        results["distances"][0]
    ):
        print("\nDistance:", distance)
        print("Content:", document[:300])

    # --------------------------------------------------
    # 4. Extract search results
    # --------------------------------------------------
    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    # --------------------------------------------------
    # 5. Filter irrelevant documents
    # --------------------------------------------------
    retrieved_chunks = []

    for document, metadata, distance in zip(
        documents,
        metadatas,
        distances
    ):

        # Skip documents beyond the threshold
        if distance > distance_threshold:
            continue

        # --------------------------------------------------
        # 6. Add relevant document with metadata
        # --------------------------------------------------
        retrieved_chunks.append({
            "content": document,
            "source": metadata.get("source"),
            "category": metadata.get("category"),
            "department": metadata.get("department"),
            "chunk_index": metadata.get("chunk_index"),
            "distance": distance
        })

    # --------------------------------------------------
    # 7. Return only relevant chunks
    # --------------------------------------------------
    return retrieved_chunks


# --------------------------------------------------
# 8. Test Retrieval Service
# --------------------------------------------------
if __name__ == "__main__":

    # --------------------------------------------------
    # 8.1 Check ChromaDB Collection
    # --------------------------------------------------
    print("Collection Name:", collection.name)
    print("Total Stored Chunks:", collection.count())

    # --------------------------------------------------
    # 8.2 Check Stored Documents
    # --------------------------------------------------
    stored_data = collection.get(
        include=["documents", "metadatas"]
    )

    print("\nStored IDs:", stored_data["ids"])

    print("\nStored Documents:")
    for document in stored_data["documents"]:
        print(document[:200])

    # --------------------------------------------------
    # 8.3 Test Retrieval
    # --------------------------------------------------
    user_question = "What is the annual leave policy?"

    results = search_documents(user_question)

    print("\nRetrieved Results:", results)
