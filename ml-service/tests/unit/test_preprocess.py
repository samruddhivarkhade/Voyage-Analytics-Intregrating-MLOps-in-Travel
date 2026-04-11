import pytest
import numpy as np
from fastapi import HTTPException

from app.schemas.input_schema import FlightPriceRequest
from app.services.preprocess import (
    build_feature_vector,
    encode_categoricals,
    FEATURE_ORDER,
    CATEGORICAL_FEATURES,
)


def make_request(**overrides):
    defaults = {
        "flightType": "economic",
        "agency": "Rainbow",
        "gender": "male",
        "distance": 1200.5,
        "time": 4.5,
        "age": 35,
    }
    defaults.update(overrides)
    return FlightPriceRequest(**defaults)


def test_feature_vector_has_correct_shape(mock_encoders):
    vector = build_feature_vector(make_request(), mock_encoders)
    assert vector.shape == (1, len(FEATURE_ORDER))


def test_feature_vector_dtype_is_float(mock_encoders):
    vector = build_feature_vector(make_request(), mock_encoders)
    assert vector.dtype == float


def test_feature_vector_preserves_exact_training_order(mock_encoders):
    request = make_request(
        flightType="economic",
        time=4.5,
        distance=1200.5,
        agency="Rainbow",
        gender="male",
        age=35,
    )
    vector = build_feature_vector(request, mock_encoders)
    expected = np.array([[0.0, 4.5, 1200.5, 2.0, 1.0, 35.0]])
    np.testing.assert_array_equal(vector, expected)


def test_numeric_features_passed_through_unchanged(mock_encoders):
    request = make_request(distance=9999.99, time=12.34, age=99)
    vector = build_feature_vector(request, mock_encoders).flatten().tolist()
    assert vector[1] == 12.34
    assert vector[2] == 9999.99
    assert vector[5] == 99.0


def test_encode_categoricals_returns_integer_values(mock_encoders):
    encoded = encode_categoricals(make_request(flightType="firstClass", agency="CloudFy", gender="female"), mock_encoders)
    assert isinstance(encoded["flightType"], int)
    assert isinstance(encoded["agency"], int)
    assert isinstance(encoded["gender"], int)


def test_encode_all_flight_types(mock_encoders):
    for flight_type, expected in [("economic", 0), ("firstClass", 1), ("premium", 2)]:
        encoded = encode_categoricals(make_request(flightType=flight_type), mock_encoders)
        assert encoded["flightType"] == expected


def test_encode_all_agencies(mock_encoders):
    for agency, expected in [("CloudFy", 0), ("FlyingDrops", 1), ("Rainbow", 2)]:
        encoded = encode_categoricals(make_request(agency=agency), mock_encoders)
        assert encoded["agency"] == expected


def test_encode_all_genders(mock_encoders):
    for gender, expected in [("female", 0), ("male", 1)]:
        encoded = encode_categoricals(make_request(gender=gender), mock_encoders)
        assert encoded["gender"] == expected


def test_unknown_category_raises_http_exception(mock_encoders):
    bad_request = FlightPriceRequest.model_construct(
        flightType="businessClass",
        agency="Rainbow",
        gender="male",
        distance=1000.0,
        time=3.0,
        age=30,
    )
    with pytest.raises(HTTPException) as exc_info:
        encode_categoricals(bad_request, mock_encoders)
    assert exc_info.value.status_code == 422
    assert exc_info.value.detail["feature"] == "flightType"


def test_unknown_category_error_detail_contains_valid_values(mock_encoders):
    bad_request = FlightPriceRequest.model_construct(
        flightType="economic",
        agency="SkyJet",
        gender="male",
        distance=1000.0,
        time=3.0,
        age=30,
    )
    with pytest.raises(HTTPException) as exc_info:
        encode_categoricals(bad_request, mock_encoders)
    detail = exc_info.value.detail
    assert "valid_values" in detail
    assert "SkyJet" not in detail["valid_values"]


def test_unknown_category_error_contains_submitted_value(mock_encoders):
    bad_request = FlightPriceRequest.model_construct(
        flightType="economic",
        agency="Rainbow",
        gender="unknown",
        distance=1000.0,
        time=3.0,
        age=30,
    )
    with pytest.raises(HTTPException) as exc_info:
        encode_categoricals(bad_request, mock_encoders)
    assert exc_info.value.detail["value"] == "unknown"
