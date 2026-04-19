from pydantic_settings import BaseSettings
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[3]
MODELS_DIR = REPO_ROOT / "models"


class Settings(BaseSettings):
    # App settings
    app_name: str = "Voyage Analytics - Flight & Gender Prediction API"
    app_version: str = "1.0.0"
    api_prefix: str = "/v1"
    
    # Database settings
    database_url: str = f"sqlite:///{REPO_ROOT / 'voyage_analytics.db'}"
    
    # JWT settings
    secret_key: str = "voyage-analytics-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # MLflow settings
    mlflow_tracking_uri: str = ""
    model_uri: str = ""
    gender_model_uri: str = ""
    
    # Model paths
    model_path: Path = MODELS_DIR / "final_model.pkl"
    encoders_path: Path = MODELS_DIR / "encoders.pkl"
    features_path: Path = MODELS_DIR / "features.pkl"
    target_encodings_path: Path = MODELS_DIR / "target_encodings.pkl"
    gender_model_path: Path = MODELS_DIR / "gender_model.pkl"
    gender_encoder_path: Path = MODELS_DIR / "gender_encoder.pkl"
    
    # Logging
    log_level: str = "INFO"

    class Config:
        env_file = ".env"


settings = Settings()
