from contextlib import asynccontextmanager
from pathlib import Path
import sys

if __package__ in (None, ""):
    sys.path.append(str(Path(__file__).resolve().parent.parent))

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import time

from app.api.routes import router
from app.core.config import settings
from app.services.model_loader import load_model, load_encoders
from app.utils.logger import get_logger

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Loading model and encoders...")
    app.state.model = load_model()
    app.state.encoders = load_encoders()
    logger.info("Startup complete. Service is ready.")
    yield
    logger.info("Shutting down Flight Price Prediction API.")


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

app.add_middleware(RequestTimingMiddleware)

app.include_router(router, prefix=settings.api_prefix)
