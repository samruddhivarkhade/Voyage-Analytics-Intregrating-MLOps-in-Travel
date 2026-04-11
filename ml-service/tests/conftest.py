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
    for col, classes in [
        ("flightType", ["economic", "firstClass", "premium"]),
        ("agency", ["CloudFy", "FlyingDrops", "Rainbow"]),
        ("gender", ["female", "male"]),
    ]:
        le = LabelEncoder()
        le.fit(classes)
        encoders[col] = le
    return encoders


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
def client(mock_model, mock_encoders, monkeypatch):
    from app.main import app
    monkeypatch.setattr("app.main.load_model", lambda: mock_model)
    monkeypatch.setattr("app.main.load_encoders", lambda: mock_encoders)
    with TestClient(app) as c:
        yield c
