from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.config import settings
from app.db import get_db
from app.rag import answer_question
from app.schemas import QueryRequest, QueryResponse, SourceChunk

router = APIRouter(prefix="/query", tags=["query"])


@router.post("", response_model=QueryResponse)
def query_documents(request: QueryRequest, db: Session = Depends(get_db)):
    if request.access_code != settings.access_code:
        raise HTTPException(status_code=401, detail="Invalid access code")
    
    answer, sources_raw = answer_question(db, request.question)

    sources = [
        SourceChunk(
            document_id=item["document_id"],
            filename=item["filename"],
            chunk_id=item["chunk_id"],
            chunk_index=item["chunk_index"],
            content=item["content"],
            distance=float(item["distance"]),
        ) for item in sources_raw
    ]

    return QueryResponse(answer=answer, sources=sources)
