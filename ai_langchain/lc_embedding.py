
from langchain_ollama import OllamaEmbeddings
from langchain_core.documents import Document


def get_embedding_model():
    return OllamaEmbeddings(
        model="nomic-embed-text"
    )


def generate_embeddings(
    chunks: list[Document],
) -> list[list[float]]:

    embedding_model = get_embedding_model()

    texts = [
        chunk.page_content
        for chunk in chunks
    ]

    embeddings = embedding_model.embed_documents(texts)

    return embeddings


if __name__ == "__main__":
    from ai_langchain.lc_document_loader import load_document
    from ai_langchain.lc_text_splitter import split_documents

    documents = load_document(
        "documents/lc_uploads/hr_policy.txt"
    )

    chunks = split_documents(documents)

    embeddings = generate_embeddings(chunks)

    print("Total chunks:", len(chunks))
    print("Total embeddings:", len(embeddings))

    print("\nFirst embedding:")
    print(embeddings[0][:10])
