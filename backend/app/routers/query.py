from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth import verify_access_code
from app.db import get_db
from app.rag import answer_question
from app.schemas import QueryRequest, QueryResponse, SourceChunk

router = APIRouter(prefix="/query", tags=["query"])


@router.post("", response_model=QueryResponse)
def query_documents(
    request: QueryRequest,
    _: None = Depends(verify_access_code),
    db: Session = Depends(get_db)
):

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
