
from pathlib import Path
from uuid import uuid4

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Form,
    HTTPException
)

from ai.ingestion_service import ingest_document

from ai.vector_store import (
    delete_document_chunks,
    get_stored_documents
)

from typing import Annotated

# --------------------------------------------------
# 1. Initialize Documents Router
# --------------------------------------------------

router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)


# --------------------------------------------------
# 2. Define Upload Directory
# --------------------------------------------------

UPLOAD_DIR = Path("documents/uploads")

UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# --------------------------------------------------
# 3. Define Allowed File Extensions
# --------------------------------------------------

ALLOWED_EXTENSIONS = {
    ".txt",
    ".pdf",
    ".docx"
}


# --------------------------------------------------
# 4. Upload Single Document
# --------------------------------------------------

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    category: str = Form(...),
    department: str = Form(...)
):

    # --------------------------------------------------
    # 4.1 Validate File Name
    # --------------------------------------------------

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="File name is required"
        )

    original_file_name = Path(file.filename).name

    # --------------------------------------------------
    # 4.2 Validate File Extension
    # --------------------------------------------------

    extension = Path(
        original_file_name
    ).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail="Only TXT, PDF and DOCX files are allowed"
        )

    # --------------------------------------------------
    # 4.3 Generate Unique Document ID
    # --------------------------------------------------

    document_id = str(uuid4())

    # --------------------------------------------------
    # 4.4 Generate Stored File Name
    # --------------------------------------------------

    stored_file_name = (
        f"{document_id}_{original_file_name}"
    )

    file_path = UPLOAD_DIR / stored_file_name

    # --------------------------------------------------
    # 4.5 Save Uploaded File
    # --------------------------------------------------

    try:
        file_content = await file.read()

        file_path.write_bytes(file_content)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to save uploaded file: {str(e)}"
        )

    finally:
        await file.close()

    # --------------------------------------------------
    # 4.6 Ingest Document into ChromaDB
    # --------------------------------------------------

    try:
        result = ingest_document(
            file_path=str(file_path),
            category=category,
            department=department,
            document_id=document_id,
            original_file_name=original_file_name
        )

    except Exception as e:

        # --------------------------------------------------
        # 4.7 Remove File if Ingestion Fails
        # --------------------------------------------------

        if file_path.exists():
            file_path.unlink()

        raise HTTPException(
            status_code=500,
            detail=f"Document ingestion failed: {str(e)}"
        )

    # --------------------------------------------------
    # 4.8 Return Upload Result
    # --------------------------------------------------

    return {
        "document_id": document_id,
        "original_file_name": original_file_name,
        "stored_file_name": stored_file_name,
        "total_chunks": result["total_chunks"],
        "status": "success",
        "message": "Document uploaded and ingested successfully"
    }


# --------------------------------------------------
# 5. Upload Multiple Documents
# --------------------------------------------------

@router.post("/upload-multiple")
async def upload_multiple_documents(
    files: list[UploadFile] = File(...),
    category: str = Form(...),
    department: str = Form(...)
):
    # --------------------------------------------------
    # 5.1 Validate Uploaded Files
    # --------------------------------------------------

    if not files:
        raise HTTPException(
            status_code=400,
            detail="Please upload at least one file"
        )

    # --------------------------------------------------
    # 5.2 Initialize Upload Results
    # --------------------------------------------------

    upload_results = []

    # --------------------------------------------------
    # 5.3 Process Each Uploaded File
    # --------------------------------------------------

    for file in files:

        # --------------------------------------------------
        # 5.3.1 Validate File Name
        # --------------------------------------------------

        if not file.filename:
            upload_results.append({
                "file_name": None,
                "status": "failed",
                "message": "File name is required"
            })

            await file.close()
            continue

        original_file_name = Path(
            file.filename
        ).name

        # --------------------------------------------------
        # 5.3.2 Validate File Extension
        # --------------------------------------------------

        extension = Path(
            original_file_name
        ).suffix.lower()

        if extension not in ALLOWED_EXTENSIONS:

            upload_results.append({
                "file_name": original_file_name,
                "status": "failed",
                "message": "Only TXT, PDF and DOCX files are allowed"
            })

            await file.close()
            continue

        # --------------------------------------------------
        # 5.3.3 Generate Unique Document ID
        # --------------------------------------------------

        document_id = str(uuid4())

        # --------------------------------------------------
        # 5.3.4 Generate Stored File Name
        # --------------------------------------------------

        stored_file_name = (
            f"{document_id}_{original_file_name}"
        )

        file_path = UPLOAD_DIR / stored_file_name

        # --------------------------------------------------
        # 5.3.5 Save and Ingest Document
        # --------------------------------------------------

        try:
            file_content = await file.read()

            file_path.write_bytes(file_content)

            result = ingest_document(
                file_path=str(file_path),
                category=category,
                department=department,
                document_id=document_id,
                original_file_name=original_file_name
            )

            # --------------------------------------------------
            # 5.3.6 Add Successful Upload Result
            # --------------------------------------------------

            upload_results.append({
                "document_id": document_id,
                "original_file_name": original_file_name,
                "stored_file_name": stored_file_name,
                "total_chunks": result["total_chunks"],
                "status": "success"
            })

        except Exception as e:

            # --------------------------------------------------
            # 5.3.7 Remove File if Processing Fails
            # --------------------------------------------------

            if file_path.exists():
                file_path.unlink()

            upload_results.append({
                "file_name": original_file_name,
                "status": "failed",
                "message": str(e)
            })

        finally:
            await file.close()

    # --------------------------------------------------
    # 5.4 Calculate Upload Summary
    # --------------------------------------------------

    successful_uploads = sum(
        1
        for result in upload_results
        if result["status"] == "success"
    )

    failed_uploads = sum(
        1
        for result in upload_results
        if result["status"] == "failed"
    )

    # --------------------------------------------------
    # 5.5 Return Multiple Upload Results
    # --------------------------------------------------

    return {
        "total_files": len(files),
        "successful_uploads": successful_uploads,
        "failed_uploads": failed_uploads,
        "results": upload_results
    }


# --------------------------------------------------
# 6. Delete Uploaded Document
# --------------------------------------------------

@router.delete("/{document_id}")
def delete_document(
    document_id: str
):

    # --------------------------------------------------
    # 6.1 Find Uploaded File
    # --------------------------------------------------

    matching_files = list(
        UPLOAD_DIR.glob(
            f"{document_id}_*"
        )
    )

    if not matching_files:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    file_path = matching_files[0]

    # --------------------------------------------------
    # 6.2 Delete ChromaDB Chunks
    # --------------------------------------------------

    try:
        delete_document_chunks(document_id)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to delete document chunks: {str(e)}"
        )

    # --------------------------------------------------
    # 6.3 Delete Uploaded File
    # --------------------------------------------------

    try:
        file_path.unlink()

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Chunks deleted, but file deletion failed: {str(e)}"
        )

    # --------------------------------------------------
    # 6.4 Return Delete Result
    # --------------------------------------------------

    return {
        "document_id": document_id,
        "file_name": file_path.name,
        "status": "success",
        "message": "Document and its ChromaDB chunks deleted successfully"
    }


# --------------------------------------------------
# 7. View Stored Documents
# --------------------------------------------------

@router.get("/")
def view_documents():

    # --------------------------------------------------
    # 7.1 Retrieve Records from ChromaDB
    # --------------------------------------------------

    results = get_stored_documents()

    # --------------------------------------------------
    # 7.2 Group Chunks by Document ID
    # --------------------------------------------------

    documents = {}

    for metadata in results["metadatas"]:

        document_id = metadata.get(
            "document_id"
        )

        if not document_id:
            continue

        # --------------------------------------------------
        # 7.3 Create Document Entry
        # --------------------------------------------------

        if document_id not in documents:

            documents[document_id] = {
                "document_id": document_id,
                "file_name": metadata.get("source"),
                "category": metadata.get("category"),
                "department": metadata.get("department"),
                "total_chunks": 0
            }

        # --------------------------------------------------
        # 7.4 Count Document Chunks
        # --------------------------------------------------

        documents[document_id]["total_chunks"] += 1

    # --------------------------------------------------
    # 7.5 Return Document List
    # --------------------------------------------------

    return {
        "total_documents": len(documents),
        "documents": list(documents.values())
    }
