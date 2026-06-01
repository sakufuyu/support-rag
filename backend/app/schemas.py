from pydantic import BaseModel


class DocumentResponse(BaseModel):
    id: int
    filename: str

    class Config:
        from_attributes = True


class SourceChunk(BaseModel):
    document_id: int
    filename: str
    chunk_id: int
    chunk_index: int
    content: str
    distance: float


class QueryRequest(BaseModel):
    question: str
    access_code: str | None = None


class QueryResponse(BaseModel):
    answer: str
    sources: list[SourceChunk]
