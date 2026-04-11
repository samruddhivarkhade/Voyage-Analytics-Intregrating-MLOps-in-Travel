import joblib
from pathlib import Path
from app.core.config import settings
from app.utils.logger import get_logger

logger = get_logger(__name__)


def load_model():
    model_path: Path = settings.model_path
    if not model_path.exists():
        logger.error("Model file not found at path: %s", model_path)
        raise FileNotFoundError(f"Model file not found: {model_path}")
    model = joblib.load(model_path)
    logger.info("Flight price model loaded from %s", model_path)
    return model


def load_encoders() -> dict:
    encoders_path: Path = settings.encoders_path
    if not encoders_path.exists():
        logger.error("Encoders file not found at path: %s", encoders_path)
        raise FileNotFoundError(f"Encoders file not found: {encoders_path}")
    encoders = joblib.load(encoders_path)
    logger.info("Regression encoders loaded from %s", encoders_path)
    return encoders
