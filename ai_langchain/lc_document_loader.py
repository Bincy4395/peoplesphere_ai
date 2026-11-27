
from pathlib import Path

from langchain_community.document_loaders import (
    TextLoader,
    PyPDFLoader,
    Docx2txtLoader,
)


def load_document(file_path: str):
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Document not found: {file_path}"
        )

    extension = path.suffix.lower()

    # TXT file
    if extension == ".txt":
        loader = TextLoader(
            str(path),
            encoding="utf-8",
        )

    # PDF file
    elif extension == ".pdf":
        loader = PyPDFLoader(str(path))

    # DOCX file
    elif extension == ".docx":
        loader = Docx2txtLoader(str(path))

    else:
        raise ValueError(
            f"Unsupported file format: {extension}"
        )

    documents = loader.load()

    return documents


if __name__ == "__main__":
    file_path = "documents/lc_uploads/hr_policy.txt"

    documents = load_document(file_path)

    for document in documents:
        print("Content:")
        print(document.page_content)

        print("\nMetadata:")
        print(document.metadata)
