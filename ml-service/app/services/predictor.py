import numpy as np
from app.utils.logger import get_logger

logger = get_logger(__name__)


def run_prediction(model, feature_vector: np.ndarray) -> float:
    prediction = model.predict(feature_vector)
    predicted_price = float(round(prediction[0], 4))
    logger.info("Prediction result: %.4f", predicted_price)
    return predicted_price
