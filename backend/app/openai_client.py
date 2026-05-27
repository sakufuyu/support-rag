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
You are a technical support assistant.

Answer the user's question using only the provided context.
If the context is not enough, say: "I don't know based on the provided documents.

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