
from ai_langchain.lc_vector_store import vector_store


def search_documents(
    query: str,
    top_k: int = 3,
    distance_threshold: float = 0.30,
):
    # 1. Search similar documents
    results = vector_store.similarity_search_with_score(
        query=query,
        k=top_k,
    )

    print("\nQuestion:", query)
    print("\nRaw Retrieved Distances:")

    for document, distance in results:
        print(distance)

    # 2. Filter relevant documents
    retrieved_chunks = []

    for document, distance in results:

        if distance > distance_threshold:
            continue

        metadata = document.metadata

        retrieved_chunks.append({
            "content": document.page_content,
            "source": metadata.get("source"),
            "category": metadata.get("category"),
            "department": metadata.get("department"),
            "chunk_index": metadata.get("chunk_index"),
            "distance": distance,
        })

    # 3. Print filtered results
    print("\nDistance Threshold:", distance_threshold)
    print("Relevant Chunks Found:", len(retrieved_chunks))

    print("\nFiltered Retrieved Documents:")

    for chunk in retrieved_chunks:
        print("\nDistance:", chunk["distance"])
        print("Content:", chunk["content"][:300])

    return retrieved_chunks


# --------------------------------------------------
# Test Retrieval Service
# --------------------------------------------------

if __name__ == "__main__":

    stored_data = vector_store.get(
        include=["documents", "metadatas"]
    )

    print("Collection Name:", vector_store._collection.name)
    print("Total Stored Chunks:", len(stored_data["ids"]))

    user_question = "What is the maternity leave policy?"

    results = search_documents(user_question)

    print("\nFinal Retrieved Results:", results)
