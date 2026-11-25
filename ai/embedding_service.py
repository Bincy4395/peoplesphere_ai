from ollama import embed


def generate_embeddings(chunks: list[str]):

    response = embed(
        model="nomic-embed-text",
        input=chunks
    )

    embeddings = response["embeddings"]

    return embeddings


if __name__ == "__main__":

    from ai.document_loader import load_document
    from ai.text_splitter import split_text

    # Step 1: Load document
    content = load_document("documents/uploads/hr_policy.txt")

    # Step 2: Split document into chunks
    chunks = split_text(content)

    # Step 3: Generate embeddings
    embeddings = generate_embeddings(chunks)

    # Step 4: Display results
    print("Total chunks:", len(chunks))
    print("Total embeddings:", len(embeddings))

    print("\nFirst chunk:")
    print(chunks[0])

    print("\nFirst embedding:")
    print(embeddings[0][:10])
