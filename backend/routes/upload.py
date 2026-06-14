from pathlib import Path
import shutil

from fastapi import APIRouter, UploadFile, File

from services.ingestion import ingest_document

router = APIRouter()

UPLOAD_DIR = Path("data/uploads")


@router.post("/upload")
async def upload_files(
    files: list[UploadFile] = File(...)
):

    uploaded = []

    for file in files:

        file_path = UPLOAD_DIR / file.filename

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(
                file.file,
                buffer
            )

        chunk_count = ingest_document(
            str(file_path)
        )

        uploaded.append({
            "name": file.filename,
            "size": file.size,
            "chunks": chunk_count
        })

    return {
        "files": uploaded
    }