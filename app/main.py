import logging
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.autentication.router import router as auth_router
from app.core.domain_exception import DomainException
from app.infra.database import create_tables, init_database

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_database()
    create_tables()
    yield

app = FastAPI(
    title="track-money",
    description="A simple app to track your money",
    version="0.1.0",
    lifespan=lifespan,
)

@app.exception_handler(DomainException)
async def domain_exception_handler(_: Request, exc: DomainException):
    logger.warning(f"DomainException: {exc.message}")
    return JSONResponse(status_code=400, content={"detail": exc.message})

app.include_router(auth_router, prefix="/users")

@app.get("/health", tags=["Health"])
async def health_check():
    return JSONResponse(content={"status": "ok"})