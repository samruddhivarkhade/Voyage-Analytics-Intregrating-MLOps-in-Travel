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
    logger.info("Label encoders loaded from %s", encoders_path)
    return encoders


def load_target_encodings() -> dict:
    target_encodings_path: Path = settings.target_encodings_path
    if not target_encodings_path.exists():
        logger.error("Target encodings file not found at path: %s", target_encodings_path)
        raise FileNotFoundError(f"Target encodings file not found: {target_encodings_path}")
    target_encodings = joblib.load(target_encodings_path)
    logger.info("Target encodings loaded from %s", target_encodings_path)
    return target_encodings


def load_selected_features() -> list:
    features_path: Path = settings.features_path
    if not features_path.exists():
        logger.warning("Selected features file not found at path: %s. Using all features.", features_path)
        return None
    features = joblib.load(features_path)
    logger.info("Selected features loaded from %s", features_path)
    return features
