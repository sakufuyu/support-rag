from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import Document, Chunk
from app.chunking import chunk_text
from app.openai_client import create_embedding
from app.schemas import DocumentResponse

router = APIRouter(prefix="/documents", tags=["documents"])


@router.post("/upload", response_model=DocumentResponse)
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    allowed_extensions = (".txt", ".md")

    if not file.filename.endswith(allowed_extensions):
        raise HTTPException(status_code=400, detail="Only .txt and .md files are supported in v1.")
    
    raw = await file.read()

    # 5 MB maximum
    if len(raw) > 5 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="File too large. Max size is 5 MB.")
    
    text = raw.decode("utf-8", errors="ignore")

    # Create a parent object in db
    document = Document(filename=file.filename)
    db.add(document)

    # Get Temporary ID for the parent object
    db.flush()

    chunks = chunk_text(text)
    for idx, content in enumerate(chunks):
        embedding = create_embedding(content)
        chunk = Chunk(
            document_id=document.id,
            chunk_index=idx,
            content=content,
            embedding=embedding,
        )
        db.add(chunk)

    # Now save the item in db.
    db.commit()
    db.refresh(document)

    return document


@router.get("", response_model=list[DocumentResponse])
def list_documents(db: Session = Depends(get_db)):
    return db.query(Document).order_by(Document.created_at.desc()).all()
