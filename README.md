# support-rag

SupportRAG is a production-style RAG web application for technical support workflows.

It allows users to upload technical documents such as runbooks, FAQs, and incident notes, then ask questions and receive source-grounded answers using OpenAI API, PostgreSQL + pgvector, FastAPI, Next.js, and AWS.

## Why I Built This

Many support engineers need to search across internal runbooks, troubleshooting guides, and incident notes. Keyword search often misses semantically related information, while general LLM answers may hallucinate.

This project demonstrates how to build a RAG system that retrieves relevant source chunks, generates grounded answers, shows citations, tracks cost/latency, and can be deployed as a web application on AWS.

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

### Infrastructure
- AWS CDK TypeScript
- S3
- CloudFront
- App Runner
- RDS PostgreSQL
- Secrets Manager
- CloudWatch

## Architecture

```text
User
  ↓
CloudFront
  ├── S3 / Next.js frontend
  └── App Runner / FastAPI backend
          ↓
      RDS PostgreSQL + pgvector
          ↓
      OpenAI API
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