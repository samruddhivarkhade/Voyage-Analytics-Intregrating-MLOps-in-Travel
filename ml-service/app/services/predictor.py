import numpy as np
from app.utils.logger import get_logger
import joblib
from app.core.config import settings
logger = get_logger(__name__)


def run_prediction(model, feature_vector: np.ndarray) -> float:
    prediction = model.predict(feature_vector)
    predicted_price = float(round(prediction[0], 4))
    logger.info("Prediction result: %.4f", predicted_price)
    return predicted_price




# Load gender model once
gender_model = joblib.load(settings.gender_model_path)
gender_encoder = joblib.load(settings.gender_encoder_path)

def predict_gender(feature_vector: np.ndarray) -> str:
    dict_data = feature_vector

    result = dict_data.values()

    print("RESULT  : " , result)

    data = list(result)

    np_arr = np.array(data,dtype=np.float64)

    pred = gender_model.predict([np_arr])
    gender = gender_encoder.inverse_transform([pred])[0]

    logger.info("Predicted gender: %s", gender)

    return gender