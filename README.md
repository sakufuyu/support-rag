# support-rag

> [!IMPORTANT]
> ## Try the Live RAG Demo
>
> TXT files containing **fictional histories of Google and Amazon** have been uploaded to the [RAG demo application](https://support-rag-portfolio.web.app/).
>
> **Open the Chat page, enter the access code `query-demo-2026`, and try asking questions about Amazon and Google.**
>
> Document uploads are restricted, and the upload access code is not publicly shared to protect the database.
>
> The demo data is entirely fictional and does not represent the actual history of, or facts about, Google or Amazon.

SupportRAG is a production-style RAG web application for technical support workflows.

It allows users to upload technical documents such as runbooks, FAQs, and incident notes, then ask questions and receive source-grounded answers using OpenAI API, PostgreSQL + pgvector, FastAPI, and Next.js.

## Demo Video

Watch the actual SupportRAG demo to see document upload, retrieval, and source-grounded chat in action:

[![Watch the SupportRAG demo on YouTube](https://img.youtube.com/vi/ByrCkwRvzG4/hqdefault.jpg)](https://www.youtube.com/watch?v=ByrCkwRvzG4)

[Watch the demo video on YouTube](https://www.youtube.com/watch?v=ByrCkwRvzG4)

## Why I Built This

Many support engineers need to search across internal runbooks, troubleshooting guides, and incident notes. Keyword search often misses semantically related information, while general LLM answers may hallucinate.

This project demonstrates how to build a RAG system that retrieves relevant source chunks, generates grounded answers, shows citations, and tracks cost and latency through a web interface.

## Tech Stack

### Backend
- Python
- FastAPI
- PostgreSQL
- pgvector
- OpenAI API

### Frontend
- Next.js
- TypeScript

### Cloud Infrastructure
- Firebase Hosting
- Google Cloud Run
- Cloud SQL for PostgreSQL
- Secret Manager

## Deployment

The application is deployed on Google Cloud in the `us-west1` region. The statically exported Next.js frontend is served by Firebase Hosting, while the FastAPI backend runs on Cloud Run and connects to Cloud SQL for PostgreSQL with pgvector. API keys, database credentials, and access codes are provided to the backend through Secret Manager rather than stored in the repository.

## Architecture

```text
Browser
  │
  ▼
Firebase Hosting
(Next.js static frontend)
  │ HTTPS
  ▼
Cloud Run
(FastAPI backend)
  ├── Cloud SQL for PostgreSQL + pgvector
  ├── OpenAI API
  └── Secret Manager
```

## RAG Pipeline
```txt
Document upload
  ↓
Text extraction
  ↓
Chunking
  ↓
OpenAI embeddings
  ↓
Store chunks + vectors in PostgreSQL/pgvector
  ↓
User question
  ↓
Question embedding
  ↓
Vector search
  ↓
Retrieve top-k chunks
  ↓
Generate source-grounded answer
  ↓
Return answer + citations
```
