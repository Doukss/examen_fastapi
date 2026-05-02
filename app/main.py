from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import api_router
from app.core.config import settings
from app.db.base import Base
from app.db.session import engine

app = FastAPI(
    title="API RESTful de Gestion des Approvisionnements",
    description="FastAPI, PostgreSQL, Cloudinary et JWT.",
    version="1.0.0",
    docs_url="/api-docs",
    redoc_url="/docs",
    openapi_url="/openapi.json",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")


@app.on_event("startup")
def create_tables() -> None:
    Base.metadata.create_all(bind=engine)


@app.get("/", tags=["Health"])
def health_check() -> dict[str, str]:
    return {"message": "API Gestion des Approvisionnements"}
