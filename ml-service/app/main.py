from contextlib import asynccontextmanager
from pathlib import Path
import sys

if __package__ in (None, ""):
    sys.path.append(str(Path(__file__).resolve().parent.parent))

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
import time

from app.api.routes import router
from app.api.auth import router as auth_router
from app.core.config import settings
from app.core.database import init_db
from app.services.model_loader import load_model, load_encoders, load_target_encodings, load_selected_features, load_gender_model, load_gender_encoder
from app.utils.logger import get_logger

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing database...")
    init_db()
    logger.info("Loading ML models and encoders...")
    app.state.model = load_model()
    app.state.encoders = load_encoders()
    app.state.target_encodings = load_target_encodings()
    app.state.selected_features = load_selected_features()
    app.state.gender_model = load_gender_model()
    app.state.gender_encoder = load_gender_encoder()
    logger.info("Startup complete. Service is ready.")
    yield
    logger.info("Shutting down Voyage Analytics API.")


class RequestTimingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start = time.perf_counter()
        response = await call_next(request)
        duration_ms = (time.perf_counter() - start) * 1000
        logger.info(
            "Request complete | method=%s path=%s status=%s duration=%.2fms",
            request.method,
            request.url.path,
            response.status_code,
            duration_ms,
        )
        return response


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(RequestTimingMiddleware)

# Include routers
app.include_router(auth_router, prefix=settings.api_prefix)
app.include_router(router, prefix=settings.api_prefix)
