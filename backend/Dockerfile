FROM python:3.12-slim

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY pyproject.toml uv.lock ./

ENV UV_PROJECT_ENVIRONMENT=/opt/venv

RUN uv sync --frozen --no-dev

COPY app ./app

ENV PATH="/opt/venv/bin:$PATH"

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
