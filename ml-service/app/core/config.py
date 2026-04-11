from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    app_name: str = "Flight Price Prediction API"
    app_version: str = "1.0.0"
    api_prefix: str = "/v1"
    model_path: Path = Path("models/flight_price_model.pkl")
    encoders_path: Path = Path("models/regression_encoders.pkl")
    log_level: str = "INFO"

    class Config:
        env_file = ".env"


settings = Settings()
