import pytest
import numpy as np
from unittest.mock import MagicMock
from sklearn.preprocessing import LabelEncoder
from fastapi.testclient import TestClient


@pytest.fixture
def mock_model():
    model = MagicMock()
    model.predict.return_value = np.array([1234.5678])
    return model


@pytest.fixture
def mock_encoders():
    encoders = {}
    le = LabelEncoder()
    le.fit(["female", "male"])
    encoders["gender"] = le
    return encoders


@pytest.fixture
def mock_target_encodings():
    return {
        "agency": {
            "CloudFy": 1500.5,
            "FlyingDrops": 1200.8,
            "Rainbow": 1800.3,
        },
        "flightType": {
            "economic": 1100.0,
            "firstClass": 2500.0,
            "premium": 1900.0,
        },
    }


@pytest.fixture
def mock_selected_features():
    return [
        "agency_te",
        "flightType_te",
        "gender",
        "distance",
        "time",
        "age",
        "age_group",
    ]


@pytest.fixture
def valid_payload():
    return {
        "flightType": "economic",
        "agency": "Rainbow",
        "gender": "male",
        "distance": 1200.5,
        "time": 4.5,
        "age": 35,
    }


@pytest.fixture
def client(mock_model, mock_encoders, mock_target_encodings, mock_selected_features, monkeypatch):
    from app.main import app
    monkeypatch.setattr("app.main.load_model", lambda: mock_model)
    monkeypatch.setattr("app.main.load_encoders", lambda: mock_encoders)
    monkeypatch.setattr("app.main.load_target_encodings", lambda: mock_target_encodings)
    monkeypatch.setattr("app.main.load_selected_features", lambda: mock_selected_features)
    with TestClient(app) as c:
        yield c
