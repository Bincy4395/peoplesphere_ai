from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_text(text: str):

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=50,
        separators=["\n\n", "\n", " ", ""]
    )

    chunks = splitter.split_text(text)

    return chunks


if __name__ == "__main__":

    from ai.document_loader import load_document

    content = load_document("documents/uploads/hr_policy.txt")

    chunks = split_text(content)

    for index, chunk in enumerate(chunks):

        print(f"\n--- Chunk {index + 1} ---")
        print(chunk)