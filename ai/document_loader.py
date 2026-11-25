
from pathlib import Path
from pypdf import PdfReader
from docx import Document


def load_document(file_path: str):

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Document not found: {file_path}"
        )

    extension = path.suffix.lower()

    # TXT file
    if extension == ".txt":
        return path.read_text(encoding="utf-8")

    # PDF file
    elif extension == ".pdf":
        reader = PdfReader(str(path))

        text = ""

        for page in reader.pages:
            text += page.extract_text() or ""

        return text

    # DOCX file
    elif extension == ".docx":
        document = Document(str(path))

        text = "\n".join(
            paragraph.text
            for paragraph in document.paragraphs
        )

        return text

    else:
        raise ValueError(
            f"Unsupported file format: {extension}"
        )



if __name__ == "__main__":
    file_path1 = "documents/uploads/hr_policy.txt"
    file_path2 = "documents/uploads/hr_policy.pdf"
    file_path3 = "documents/uploads/hr_policy.docx"

    content = load_document(file_path1)
    print(content)