from sqlalchemy import text
from sqlalchemy.orm import Session

from app.openai_client import create_embedding, generate_answer


def retrieve_chunks(db: Session, question: str, top_k: int = 5) -> list[dict]:
    question_embedding = create_embedding(question)

    sql = text(
        # This SQL query uses `pgvector` a extension of PostgreSQL.
        # "<=>": Cosine distance operator
        # Calculate the angle between two vectors (cosine similarity); 
        # the closer the value is to 0, the more similar the meanings of the sentences are.

        # Sort the results by similarity using ORDER BY clause 
        # and use the top_k to retrieve the K texts that are most closely related in meaning.
        """
        SELECT
            chunks.id AS chunk_id,
            chunks.document_id AS document_id,
            documents.filename AS filename,
            chunks.chunk_index AS chunk_index,
            chunks.content AS content,
            chunks.embedding <=> CAST(:embedding AS vector) AS distance
        FROM chunks
        JOIN documents ON documents.id = chunks.document_id
        ORDER BY chunks.embedding <=> CAST(:embedding AS vector)
        LIMIT :top_k
        """
    )

    embedding_str = "[" + ",".join(str(x) for x in question_embedding) + "]"

    rows = db.execute(
        sql,
        {"embedding": embedding_str, "top_k": top_k},
    ).mappings().all()

    return [dict(row) for row in rows]


def answer_question(db: Session, question: str) -> tuple[str, list[dict]]:
    retrieved = retrieve_chunks(db, question, top_k=5)
    contexts = [item["content"] for item in retrieved]

    if not contexts:
        return "I dont't know based on the provided documents.", []
    
    answer = generate_answer(question, contexts)

    return answer, retrieved
