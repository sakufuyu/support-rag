from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import health, documents, query

app = FastAPI(title="SupportRAG API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(documents.router)
app.include_router(query.router)
