from openai import OpenAI
from app.config import settings


client = OpenAI(api_key=settings.openai_api_key)

EMBEDDING_MODEL = "text-embedding-3-small"
GENERATION_MODEL = "gpt-4.1-nano"


def create_embedding(text: str) -> list[float]:
    response = client.embeddings.create(
        model=EMBEDDING_MODEL,
        input=text,
    )

    return response.data[0].embedding


def generate_answer(question: str, contexts: list[str]) -> str:
    context_text = "\n\n---\n\n".join(contexts)

    prompt = f"""
You are a retrieval-augmented generation assistant.

Answer using only the retrieved context. Treat the retrieved context as authoritative for this task, even when it conflicts with your general knowledge or describes unusual events.

Do not correct the retrieved context using outside knowledge.
Do not reject a claim merely because it appears historically inaccurate.

The question and context may be written in different languages.
Answer in the same language as the user's question.

If the context supports only part of the question, answer the supported part.
Only say "I don't know based on the provided documents." when the retrieved context contains no information relevant to the question.

Context:
{context_text}

Question:
{question}
"""

    response = client.responses.create(
        model=GENERATION_MODEL,
        input=prompt,
    )

    print()
    print(response)
    print()

    return response.output_text