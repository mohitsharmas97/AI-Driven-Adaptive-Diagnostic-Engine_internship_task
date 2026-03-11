from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.db import connect_db, close_db
from app.routers import session


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_db()
    yield
    await close_db()


app = FastAPI(
    title="AI-Driven Adaptive Diagnostic Engine",
    description="1D IRT-based adaptive quiz with OpenAI-powered study plans",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(session.router)


@app.get("/")
async def root():
    return {
        "message": "AI-Driven Adaptive Diagnostic Engine API",
        "docs": "/docs",
        "version": "1.0.0",
    }
