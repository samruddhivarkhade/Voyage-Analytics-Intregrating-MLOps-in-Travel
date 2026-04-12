import numpy as np
from fastapi import HTTPException, status
from app.schemas.input_schema import FlightPriceRequest
from app.utils.logger import get_logger

logger = get_logger(__name__)


def apply_target_encoding(value: str, feature_name: str, target_encodings: dict) -> float:
    """Apply target encoding to a categorical feature."""
    if feature_name not in target_encodings:
        logger.warning("No target encoding mapping found for feature '%s'", feature_name)
        return np.nan
    
    encoding_map = target_encodings[feature_name]
    if value in encoding_map:
        return encoding_map[value]
    else:
        logger.warning("Unknown value '%s' for feature '%s', using global mean approximation", value, feature_name)
        return np.mean(list(encoding_map.values()))


def encode_label(value: str, feature_name: str, encoders: dict) -> int:
    """Apply label encoding to a categorical feature."""
    if feature_name not in encoders:
        logger.error("No label encoder found for feature '%s'", feature_name)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Missing label encoder for {feature_name}",
        )
    
    encoder = encoders[feature_name]
    known_classes = list(encoder.classes_)
    if value not in known_classes:
        logger.warning("Unknown category '%s' for feature '%s'", value, feature_name)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "feature": feature_name,
                "value": value,
                "valid_values": known_classes,
                "error": "Unknown category value",
            },
        )
    return int(encoder.transform([value])[0])


def build_feature_vector(
    request: FlightPriceRequest,
    encoders: dict,
    target_encodings: dict,
    selected_features: list = None
) -> np.ndarray:
    """Build feature vector from request."""
    raw = request.model_dump()
    
    features_dict = {}
    
    for col in ["agency", "flightType"]:
        if col in raw:
            features_dict[f"{col}_te"] = apply_target_encoding(raw[col], col, target_encodings)
    
    features_dict["gender"] = encode_label(raw["gender"], "gender", encoders)
    
    features_dict["distance"] = raw.get("distance", 0.0)
    features_dict["time"] = raw.get("time", 0.0)
    features_dict["age"] = float(raw.get("age", 0))
    
    age = raw.get("age", 0)
    if age <= 17:
        features_dict["age_group"] = 0
    elif age <= 25:
        features_dict["age_group"] = 1
    elif age <= 35:
        features_dict["age_group"] = 2
    elif age <= 50:
        features_dict["age_group"] = 3
    elif age <= 65:
        features_dict["age_group"] = 4
    else:
        features_dict["age_group"] = 5
    
    if selected_features:
        filtered_features = {}
        for feat in selected_features:
            if feat in features_dict:
                filtered_features[feat] = features_dict[feat]
            else:
                logger.warning("Selected feature '%s' not available in request data", feat)
                filtered_features[feat] = 0.0
        features_dict = filtered_features
        feature_order = selected_features
    else:
        feature_order = ["agency_te", "flightType_te", "gender", "distance", "time", "age", "age_group"]
    
    feature_values = [features_dict.get(feat, 0.0) for feat in feature_order]
    
    feature_array = np.array(feature_values, dtype=float).reshape(1, -1)
    logger.info("Feature vector built with %d features: %s", len(feature_values), feature_values)
    return feature_array
