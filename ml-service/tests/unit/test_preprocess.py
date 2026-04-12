import pytest
import numpy as np
from fastapi import HTTPException

from app.schemas.input_schema import FlightPriceRequest
from app.services.preprocess import (
    build_feature_vector,
    apply_target_encoding,
    encode_label,
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


def test_feature_vector_returns_numpy_array(mock_encoders, mock_target_encodings, mock_selected_features):
    vector = build_feature_vector(make_request(), mock_encoders, mock_target_encodings, mock_selected_features)
    assert isinstance(vector, np.ndarray)


def test_feature_vector_dtype_is_float(mock_encoders, mock_target_encodings, mock_selected_features):
    vector = build_feature_vector(make_request(), mock_encoders, mock_target_encodings, mock_selected_features)
    assert vector.dtype == float


def test_feature_vector_has_correct_shape_with_selected_features(mock_encoders, mock_target_encodings, mock_selected_features):
    vector = build_feature_vector(make_request(), mock_encoders, mock_target_encodings, mock_selected_features)
    assert vector.shape == (1, len(mock_selected_features))


def test_feature_vector_without_selected_features(mock_encoders, mock_target_encodings):
    vector = build_feature_vector(make_request(), mock_encoders, mock_target_encodings, selected_features=None)
    assert vector.shape == (1, 7)


def test_numeric_features_passed_through_unchanged(mock_encoders, mock_target_encodings, mock_selected_features):
    request = make_request(distance=9999.99, time=12.34, age=99)
    vector = build_feature_vector(request, mock_encoders, mock_target_encodings, mock_selected_features).flatten()
    dist_idx = mock_selected_features.index("distance") if "distance" in mock_selected_features else -1
    time_idx = mock_selected_features.index("time") if "time" in mock_selected_features else -1
    age_idx = mock_selected_features.index("age") if "age" in mock_selected_features else -1
    
    if dist_idx >= 0:
        assert vector[dist_idx] == 9999.99
    if time_idx >= 0:
        assert vector[time_idx] == 12.34
    if age_idx >= 0:
        assert vector[age_idx] == 99.0


def test_target_encoding_applied_to_agency(mock_encoders, mock_target_encodings, mock_selected_features):
    request = make_request(agency="CloudFy")
    vector = build_feature_vector(request, mock_encoders, mock_target_encodings, mock_selected_features)
    agency_te_idx = mock_selected_features.index("agency_te") if "agency_te" in mock_selected_features else -1
    if agency_te_idx >= 0:
        assert vector[0, agency_te_idx] == 1500.5


def test_target_encoding_applied_to_flight_type(mock_encoders, mock_target_encodings, mock_selected_features):
    request = make_request(flightType="firstClass")
    vector = build_feature_vector(request, mock_encoders, mock_target_encodings, mock_selected_features)
    flighttype_te_idx = mock_selected_features.index("flightType_te") if "flightType_te" in mock_selected_features else -1
    if flighttype_te_idx >= 0:
        assert vector[0, flighttype_te_idx] == 2500.0


def test_gender_label_encoding(mock_encoders, mock_target_encodings, mock_selected_features):
    request = make_request(gender="female")
    vector = build_feature_vector(request, mock_encoders, mock_target_encodings, mock_selected_features)
    gender_idx = mock_selected_features.index("gender") if "gender" in mock_selected_features else -1
    if gender_idx >= 0:
        assert vector[0, gender_idx] == 0


def test_age_group_calculation_young(mock_encoders, mock_target_encodings, mock_selected_features):
    request = make_request(age=15)
    vector = build_feature_vector(request, mock_encoders, mock_target_encodings, mock_selected_features)
    age_group_idx = mock_selected_features.index("age_group") if "age_group" in mock_selected_features else -1
    if age_group_idx >= 0:
        assert vector[0, age_group_idx] == 0


def test_age_group_calculation_adult(mock_encoders, mock_target_encodings, mock_selected_features):
    request = make_request(age=35)
    vector = build_feature_vector(request, mock_encoders, mock_target_encodings, mock_selected_features)
    age_group_idx = mock_selected_features.index("age_group") if "age_group" in mock_selected_features else -1
    if age_group_idx >= 0:
        assert vector[0, age_group_idx] == 2


def test_age_group_calculation_senior(mock_encoders, mock_target_encodings, mock_selected_features):
    request = make_request(age=70)
    vector = build_feature_vector(request, mock_encoders, mock_target_encodings, mock_selected_features)
    age_group_idx = mock_selected_features.index("age_group") if "age_group" in mock_selected_features else -1
    if age_group_idx >= 0:
        assert vector[0, age_group_idx] == 5


def test_unknown_gender_raises_http_exception(mock_encoders, mock_target_encodings, mock_selected_features):
    bad_request = FlightPriceRequest.model_construct(
        flightType="economic",
        agency="Rainbow",
        gender="unknown_gender",
        distance=1000.0,
        time=3.0,
        age=30,
    )
    with pytest.raises(HTTPException) as exc_info:
        build_feature_vector(bad_request, mock_encoders, mock_target_encodings, mock_selected_features)
    assert exc_info.value.status_code == 422


def test_apply_target_encoding_known_value(mock_target_encodings):
    result = apply_target_encoding("CloudFy", "agency", mock_target_encodings)
    assert result == 1500.5


def test_apply_target_encoding_unknown_value(mock_target_encodings):
    result = apply_target_encoding("UnknownAgency", "agency", mock_target_encodings)
    expected_mean = np.mean([1500.5, 1200.8, 1800.3])
    assert result == expected_mean
