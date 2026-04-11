import numpy as np
from fastapi import HTTPException, status
from app.schemas.input_schema import FlightPriceRequest
from app.utils.logger import get_logger

logger = get_logger(__name__)

FEATURE_ORDER = ["flightType", "time", "distance", "agency", "gender", "age"]
CATEGORICAL_FEATURES = ["flightType", "agency", "gender"]


def encode_categoricals(request: FlightPriceRequest, encoders: dict) -> dict:
    raw = request.model_dump()
    encoded = {}
    for feature in CATEGORICAL_FEATURES:
        encoder = encoders[feature]
        value = raw[feature]
        known_classes = list(encoder.classes_)
        if value not in known_classes:
            logger.warning("Unknown category '%s' for feature '%s'", value, feature)
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail={
                    "feature": feature,
                    "value": value,
                    "valid_values": known_classes,
                    "error": "Unknown category value",
                },
            )
        encoded[feature] = int(encoder.transform([value])[0])
    return encoded


def build_feature_vector(request: FlightPriceRequest, encoders: dict) -> np.ndarray:
    raw = request.model_dump()
    encoded_cats = encode_categoricals(request, encoders)

    feature_values = []
    for feature in FEATURE_ORDER:
        if feature in CATEGORICAL_FEATURES:
            feature_values.append(encoded_cats[feature])
        else:
            feature_values.append(raw[feature])

    feature_array = np.array(feature_values, dtype=float).reshape(1, -1)
    logger.info("Feature vector built: %s", feature_values)
    return feature_array
