import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os
import json
import logging

try:
    import mlflow
    import mlflow.sklearn
except ImportError as exc:
    raise ImportError(
        "mlflow is required for experiment tracking. Install it with: pip install mlflow"
    ) from exc

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

os.makedirs("models", exist_ok=True)
os.makedirs("reports", exist_ok=True)

MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "file:./mlruns")
MLFLOW_EXPERIMENT_NAME = os.getenv("MLFLOW_EXPERIMENT_NAME", "gender-classification")
MLFLOW_REGISTERED_MODEL_NAME = os.getenv("MLFLOW_REGISTERED_MODEL_NAME", "gender-classification-model")

mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
mlflow.set_experiment(MLFLOW_EXPERIMENT_NAME)

flights = pd.read_csv("data/flights.csv")
hotels = pd.read_csv("data/hotels.csv")
users = pd.read_csv("data/users.csv")

logger.info("Data loaded: flights=%s, hotels=%s, users=%s", flights.shape, hotels.shape, users.shape)

flight_data = pd.merge(flights, users, left_on="userCode", right_on="code")
hotel_data = pd.merge(hotels, users, left_on="userCode", right_on="code")

flight_features = flight_data.groupby("userCode").agg({
    "price": "mean",
    "distance": "mean",
    "time": "mean"
}).reset_index()

hotel_features = hotel_data.groupby("userCode").agg({
    "total": "mean",
    "days": "mean"
}).reset_index()

user_behavior = pd.merge(flight_features, hotel_features, on="userCode", how="outer")

user_behavior = pd.merge(user_behavior, users, left_on="userCode", right_on="code")

user_behavior = user_behavior.fillna(0)

df = user_behavior.copy()

le = LabelEncoder()
df['gender'] = le.fit_transform(df['gender'])

joblib.dump(le, "models/gender_encoder.pkl")

df = df.drop(['userCode', 'code', 'name', 'company'], axis=1)

X = df.drop('gender', axis=1)
y = df['gender']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

logger.info("Train/test split: train=%s, test=%s", X_train.shape, X_test.shape)

with mlflow.start_run(run_name="gender-classification-training"):
    mlflow.set_tag("project", "voyage-analytics")
    mlflow.set_tag("task", "classification")
    mlflow.log_params(
        {
            "model_type": "LogisticRegression",
            "max_iter": 200,
            "test_size": 0.2,
            "random_state": 42,
            "train_samples": int(X_train.shape[0]),
            "test_samples": int(X_test.shape[0]),
            "num_features": int(X_train.shape[1]),
        }
    )

    model = LogisticRegression(max_iter=200)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)

    y_pred_labels = le.inverse_transform(y_pred)
    y_test_labels = le.inverse_transform(y_test)

    accuracy = accuracy_score(y_test, y_pred)
    
    mlflow.log_metric("accuracy", accuracy)

    logger.info("Model accuracy: %.4f", accuracy)
    logger.info("\nClassification Report:\n%s", classification_report(y_test_labels, y_pred_labels))

    joblib.dump(model, "models/gender_model.pkl")
    joblib.dump(le, "models/gender_encoder.pkl")

    mlflow.log_artifact("models/gender_model.pkl", artifact_path="local_artifacts")
    mlflow.log_artifact("models/gender_encoder.pkl", artifact_path="local_artifacts")

    model_info = mlflow.sklearn.log_model(
        sk_model=model,
        artifact_path="model",
        registered_model_name=MLFLOW_REGISTERED_MODEL_NAME,
    )

    report = {
        "model": "LogisticRegression",
        "accuracy": float(accuracy),
        "mlflow_tracking_uri": MLFLOW_TRACKING_URI,
        "mlflow_experiment": MLFLOW_EXPERIMENT_NAME,
        "mlflow_registered_model": MLFLOW_REGISTERED_MODEL_NAME,
        "mlflow_model_uri": model_info.model_uri,
    }

    with open("reports/gender_report.json", "w") as f:
        json.dump(report, f, indent=2)

    mlflow.log_artifact("reports/gender_report.json")

    logger.info("Best model registered to MLflow model registry name: %s", MLFLOW_REGISTERED_MODEL_NAME)

logger.info("Gender classification model training completed successfully with MLflow tracking.")