import numpy as np
from unittest.mock import MagicMock

from app.services.predictor import run_prediction


SAMPLE_VECTOR = np.array([[0.0, 4.5, 1200.5, 2.0, 1.0, 35.0]])


def test_run_prediction_returns_float(mock_model):
    result = run_prediction(mock_model, SAMPLE_VECTOR)
    assert isinstance(result, float)


def test_run_prediction_calls_model_predict_once(mock_model):
    run_prediction(mock_model, SAMPLE_VECTOR)
    mock_model.predict.assert_called_once_with(SAMPLE_VECTOR)


def test_run_prediction_passes_exact_vector_to_model(mock_model):
    run_prediction(mock_model, SAMPLE_VECTOR)
    call_args = mock_model.predict.call_args[0][0]
    np.testing.assert_array_equal(call_args, SAMPLE_VECTOR)


def test_run_prediction_rounds_to_four_decimal_places():
    model = MagicMock()
    model.predict.return_value = np.array([1234.567891234])
    result = run_prediction(model, SAMPLE_VECTOR)
    assert result == round(1234.567891234, 4)


def test_run_prediction_returns_scalar_not_array(mock_model):
    result = run_prediction(mock_model, SAMPLE_VECTOR)
    assert not hasattr(result, "__len__")


def test_run_prediction_with_zero_price():
    model = MagicMock()
    model.predict.return_value = np.array([0.0])
    result = run_prediction(model, SAMPLE_VECTOR)
    assert result == 0.0


def test_run_prediction_with_large_price():
    model = MagicMock()
    model.predict.return_value = np.array([99999.9999])
    result = run_prediction(model, SAMPLE_VECTOR)
    assert result == 99999.9999


def test_run_prediction_with_high_precision_price():
    model = MagicMock()
    model.predict.return_value = np.array([500.123456789])
    result = run_prediction(model, SAMPLE_VECTOR)
    assert result == 500.1235
