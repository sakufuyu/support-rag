from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import health, documents, query

app = FastAPI(title="SupportRAG API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://d126ozpzhxt50u.cloudfront.net"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix="/api")
app.include_router(documents.router, prefix="/api")
app.include_router(query.router, prefix="/api")
