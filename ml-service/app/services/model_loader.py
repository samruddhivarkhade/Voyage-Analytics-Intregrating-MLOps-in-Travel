import joblib
from pathlib import Path
from app.core.config import settings
from app.utils.logger import get_logger

try:
    import mlflow
    import mlflow.sklearn
except ImportError:  # pragma: no cover - handled by runtime config
    mlflow = None

logger = get_logger(__name__)


def load_model():
    if settings.model_uri:
        if mlflow is None:
            raise ImportError(
                "MLflow is required to load model_uri. Install mlflow or unset MODEL_URI."
            )
        if settings.mlflow_tracking_uri:
            mlflow.set_tracking_uri(settings.mlflow_tracking_uri)
        logger.info("Loading flight price model from MLflow URI: %s", settings.model_uri)
        model = mlflow.sklearn.load_model(settings.model_uri)
        logger.info("Flight price model loaded from MLflow URI: %s", settings.model_uri)
        return model

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


def load_gender_model():
    if settings.gender_model_uri:
        if mlflow is None:
            raise ImportError(
                "MLflow is required to load gender_model_uri. Install mlflow or unset GENDER_MODEL_URI."
            )
        if settings.mlflow_tracking_uri:
            mlflow.set_tracking_uri(settings.mlflow_tracking_uri)
        logger.info("Loading gender classification model from MLflow URI: %s", settings.gender_model_uri)
        model = mlflow.sklearn.load_model(settings.gender_model_uri)
        logger.info("Gender classification model loaded from MLflow URI: %s", settings.gender_model_uri)
        return model

    gender_model_path: Path = settings.gender_model_path
    if not gender_model_path.exists():
        logger.error("Gender model file not found at path: %s", gender_model_path)
        raise FileNotFoundError(f"Gender model file not found: {gender_model_path}")
    model = joblib.load(gender_model_path)
    logger.info("Gender classification model loaded from %s", gender_model_path)
    return model


def load_gender_encoder():
    gender_encoder_path: Path = settings.gender_encoder_path
    if not gender_encoder_path.exists():
        logger.error("Gender encoder file not found at path: %s", gender_encoder_path)
        raise FileNotFoundError(f"Gender encoder file not found: {gender_encoder_path}")
    encoder = joblib.load(gender_encoder_path)
    logger.info("Gender encoder loaded from %s", gender_encoder_path)
    return encoder
