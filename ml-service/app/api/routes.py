from fastapi import APIRouter, Request
from app.schemas.input_schema import FlightPriceRequest, FlightPriceResponse
from app.services.preprocess import build_feature_vector
from app.services.predictor import run_prediction
from app.utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter()


@router.get("/health")
def health_check():
    return {"status": "healthy"}


@router.post("/predict", response_model=FlightPriceResponse)
def predict_flight_price(payload: FlightPriceRequest, request: Request):
    logger.info(
        "Incoming prediction request | client=%s | payload=%s",
        request.client.host,
        payload.model_dump(),
    )

    model = request.app.state.model
    encoders = request.app.state.encoders
    target_encodings = request.app.state.target_encodings
    selected_features = request.app.state.selected_features

    feature_vector = build_feature_vector(payload, encoders, target_encodings, selected_features)
    predicted_price = run_prediction(model, feature_vector)

    logger.info("Prediction response | predicted_price=%.4f", predicted_price)
    return FlightPriceResponse(predicted_price=predicted_price)
