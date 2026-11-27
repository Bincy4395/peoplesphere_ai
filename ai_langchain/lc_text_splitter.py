
from langchain_text_splitters import RecursiveCharacterTextSplitter

from ai_langchain.lc_document_loader import load_document


def split_documents(documents):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=50,
        separators=["\n\n", "\n", " ", ""],
    )

    chunks = text_splitter.split_documents(documents)

    return chunks


if __name__ == "__main__":
    file_path = "documents/lc_uploads/hr_policy.txt"

    documents = load_document(file_path)

    chunks = split_documents(documents)

    print(f"Total chunks: {len(chunks)}")

    for index, chunk in enumerate(chunks, start=1):
        print(f"\n--- Chunk {index} ---")
        print(chunk.page_content)
        print("Metadata:", chunk.metadata)
