from pydantic_settings import BaseSettings
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
MODELS_DIR = REPO_ROOT / "models"


class Settings(BaseSettings):
    app_name: str = "Flight Price Prediction API"
    app_version: str = "1.0.0"
    api_prefix: str = "/v1"
    mlflow_tracking_uri: str = ""
    model_uri: str = ""
    gender_model_uri: str = ""
    model_path: Path = MODELS_DIR / "final_model.pkl"
    encoders_path: Path = MODELS_DIR / "encoders.pkl"
    features_path: Path = MODELS_DIR / "features.pkl"
    target_encodings_path: Path = MODELS_DIR / "target_encodings.pkl"
    log_level: str = "INFO"
    gender_model_path: Path = MODELS_DIR / "gender_model.pkl"
    gender_encoder_path: Path = MODELS_DIR / "gender_encoder.pkl"

    class Config:
        env_file = ".env"


settings = Settings()
