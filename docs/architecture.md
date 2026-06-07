# Architecture

## Local Architecture

```text
Next.js frontend
  ↓
FastAPI backend
  ↓
PostgreSQL + pgvector
  ↓
OpenAI API
```

## AWS Architecture
```txt
User
  ↓
CloudFront
  ├── S3 frontend
  └── App Runner backend
        ↓
      RDS PostgreSQL + pgvector
        ↓
      OpenAI API
```

## Key Design Decisions

### Why custom RAG?

I implemented the core RAG pipeline myself to understand and demonstrate chunking, embeddings, retrieval, citation mapping, and evaluation.

### Why PostgreSQL + pgvector?

PostgreSQL provides a familiar relational database while pgvector enables vector similarity search in the same system.

### Why App Runner?

FastAPI is a long-running API server. App Runner allows the backend container to run as a managed web service without managing ECS directly.

### Why OpenAI API?

OpenAI provides high-quality embedding and text generation APIs, allowing this project to focus on RAG architecture, evaluation, and application deployment.