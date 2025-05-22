from fastapi import APIRouter, UploadFile, File
from pathlib import Path

router = APIRouter()

INDEX_PATH = Path("app/rag/index/faiss_index.bin")
DOCS_PATH = Path("app/rag/index/docstore.pkl")
DOCS_DIR = Path("app/rag/documents")
DOCS_DIR.mkdir(parents=True, exist_ok=True)


@router.delete("/reset-knowledge-base")
async def reset_knowledge_base():
    for file in DOCS_DIR.iterdir():
        if file.is_file():
            file.unlink()
    if INDEX_PATH.exists():
        INDEX_PATH.unlink()
    if DOCS_PATH.exists():
        DOCS_PATH.unlink()
    return {"message": "Knowledge base reset successfully."}


@router.post("/upload")
async def upload(file: UploadFile = File(...)):
    if not file.filename.endswith(".txt"):
        return {"error": "Only .txt files are allowed."}

    destination = DOCS_DIR / file.filename
    with destination.open("wb") as f:
        f.write(await file.read())

    return {"message": f"{file.filename} uploaded successfully."}
