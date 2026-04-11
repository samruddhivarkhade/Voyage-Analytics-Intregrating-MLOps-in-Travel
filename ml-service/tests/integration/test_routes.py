import pytest


def test_health_returns_200(client):
    response = client.get("/v1/health")
    assert response.status_code == 200


def test_health_returns_healthy_status(client):
    response = client.get("/v1/health")
    assert response.json() == {"status": "healthy"}


def test_predict_valid_payload_returns_200(client, valid_payload):
    response = client.post("/v1/predict", json=valid_payload)
    assert response.status_code == 200


def test_predict_response_contains_predicted_price_key(client, valid_payload):
    response = client.post("/v1/predict", json=valid_payload)
    assert "predicted_price" in response.json()


def test_predict_predicted_price_is_float(client, valid_payload):
    body = client.post("/v1/predict", json=valid_payload).json()
    assert isinstance(body["predicted_price"], float)


def test_predict_predicted_price_matches_mock_model(client, valid_payload):
    body = client.post("/v1/predict", json=valid_payload).json()
    assert body["predicted_price"] == 1234.5678


def test_predict_invalid_flight_type_returns_422(client, valid_payload):
    valid_payload["flightType"] = "businessClass"
    assert client.post("/v1/predict", json=valid_payload).status_code == 422


def test_predict_invalid_agency_returns_422(client, valid_payload):
    valid_payload["agency"] = "SkyJet"
    assert client.post("/v1/predict", json=valid_payload).status_code == 422


def test_predict_invalid_gender_returns_422(client, valid_payload):
    valid_payload["gender"] = "nonbinary"
    assert client.post("/v1/predict", json=valid_payload).status_code == 422


def test_predict_missing_distance_returns_422(client, valid_payload):
    del valid_payload["distance"]
    assert client.post("/v1/predict", json=valid_payload).status_code == 422


def test_predict_missing_age_returns_422(client, valid_payload):
    del valid_payload["age"]
    assert client.post("/v1/predict", json=valid_payload).status_code == 422


def test_predict_missing_flight_type_returns_422(client, valid_payload):
    del valid_payload["flightType"]
    assert client.post("/v1/predict", json=valid_payload).status_code == 422


def test_predict_missing_agency_returns_422(client, valid_payload):
    del valid_payload["agency"]
    assert client.post("/v1/predict", json=valid_payload).status_code == 422


def test_predict_empty_body_returns_422(client):
    assert client.post("/v1/predict", json={}).status_code == 422


def test_predict_all_valid_flight_types_return_200(client, valid_payload):
    for flight_type in ["economic", "firstClass", "premium"]:
        valid_payload["flightType"] = flight_type
        assert client.post("/v1/predict", json=valid_payload).status_code == 200


def test_predict_all_valid_agencies_return_200(client, valid_payload):
    for agency in ["Rainbow", "CloudFy", "FlyingDrops"]:
        valid_payload["agency"] = agency
        assert client.post("/v1/predict", json=valid_payload).status_code == 200


def test_predict_all_valid_genders_return_200(client, valid_payload):
    for gender in ["male", "female"]:
        valid_payload["gender"] = gender
        assert client.post("/v1/predict", json=valid_payload).status_code == 200


def test_predict_zero_distance_returns_200(client, valid_payload):
    valid_payload["distance"] = 0.0
    assert client.post("/v1/predict", json=valid_payload).status_code == 200


def test_predict_large_values_return_200(client, valid_payload):
    valid_payload["distance"] = 99999.0
    valid_payload["time"] = 999.0
    valid_payload["age"] = 120
    assert client.post("/v1/predict", json=valid_payload).status_code == 200


def test_predict_wrong_method_get_returns_405(client):
    assert client.get("/v1/predict").status_code == 405


def test_unknown_route_returns_404(client):
    assert client.get("/v1/unknown").status_code == 404
