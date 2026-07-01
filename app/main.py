import logging
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.autentication import router as auth_router
from app.core.domain_error import DomainError
from app.infra.database import create_tables, init_database
from app.movement import router as movement_router
from app.subscription import router as subscription_router

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

@app.exception_handler(DomainError)
async def domain_error_handler(_: Request, exc: DomainError):
    logger.warning(f"DomainError: {exc.message}")
    return JSONResponse(status_code=400, content={"detail": exc.message})

app.include_router(auth_router, prefix="/users")
app.include_router(subscription_router, prefix="/subscription")
app.include_router(movement_router, prefix="/movement")

@app.get("/health", tags=["Health"])
async def health_check():
    return JSONResponse(content={"status": "ok"})