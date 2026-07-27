import logging
import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.authentication import router as auth_router
from app.core.domain_error import DomainError
from app.infra.database import create_tables, get_session_local, init_database
from app.movement import router as movement_router
from app.subscription import router as subscription_router
from app.subscription.plan._plan_repository import PlanRepository
from app.subscription.use_cases.seed_default_plans import seed_default_plans

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()


def get_frontend_origins() -> list[str]:
    configured_origins = os.getenv("FRONTEND_ORIGINS")
    if configured_origins:
        return [
            origin.strip()
            for origin in configured_origins.split(",")
            if origin.strip()
        ]

    return [
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "http://127.0.0.1:8080",
        "http://localhost:8080",
    ]


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_database()
    create_tables()
    db = get_session_local()()
    try:
        seed_default_plans(PlanRepository(db))
    finally:
        db.close()
    yield


app = FastAPI(
    title="track-money",
    description="A simple app to track your money",
    version="0.1.0",
    lifespan=lifespan,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=get_frontend_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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