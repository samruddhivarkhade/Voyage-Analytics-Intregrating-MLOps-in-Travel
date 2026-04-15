import pandas as pd
import numpy as np
import logging
import os
import json
import joblib
import time

from sklearn.model_selection import train_test_split, KFold, cross_val_score
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.feature_selection import mutual_info_regression

from sklearn.linear_model import LinearRegression, Ridge
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor

from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

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
MLFLOW_EXPERIMENT_NAME = os.getenv("MLFLOW_EXPERIMENT_NAME", "flight-price-prediction")
MLFLOW_REGISTERED_MODEL_NAME = os.getenv("MLFLOW_REGISTERED_MODEL_NAME", "flight-price-model")

mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
mlflow.set_experiment(MLFLOW_EXPERIMENT_NAME)


flights = pd.read_csv("data/flights.csv")
users   = pd.read_csv("data/users.csv")

df = pd.merge(flights, users, left_on="userCode", right_on="code")


df = df.sample(n=50000, random_state=42)

logger.info(f"Data loaded: {df.shape}")


df['date'] = pd.to_datetime(df['date'], errors='coerce')
df['day_of_week'] = df['date'].dt.dayofweek
df['month'] = df['date'].dt.month
df['is_weekend'] = (df['day_of_week'] >= 5).astype(int)
df['route'] = df['from'].astype(str) + "_" + df['to'].astype(str)

df['age_group'] = pd.cut(df['age'],
                        bins=[0,17,25,35,50,65,120],
                        labels=[0,1,2,3,4,5]).astype(float)

TARGET = "price"

X = df.drop(columns=[TARGET])
y = df[TARGET]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

logger.info(f"Split: train={X_train.shape}, test={X_test.shape}")


target_encode_mappings = {}

def target_encode(train, test, col, target, smoothing=10):
    stats = train.groupby(col)[target].agg(['mean', 'count'])
    global_mean = train[target].mean()
    smooth = (stats['mean'] * stats['count'] + global_mean * smoothing) / (stats['count'] + smoothing)

    train[col+"_te"] = train[col].map(smooth)
    test[col+"_te"] = test[col].map(smooth)

    target_encode_mappings[col] = smooth.to_dict()
    return train, test

for col in ["route", "agency", "flightType"]:
    if col in X_train.columns:
        X_train[col] = X_train[col].astype(str)
        X_test[col] = X_test[col].astype(str)

        X_train[col+"_target"] = y_train
        X_train, X_test = target_encode(X_train, X_test, col, col+"_target")
        X_train = X_train.drop(columns=[col+"_target"])


drop_cols = ['date','from','to','route','userCode','code','name','company','agency','flightType']
X_train = X_train.drop(columns=[c for c in drop_cols if c in X_train.columns])
X_test  = X_test.drop(columns=[c for c in drop_cols if c in X_test.columns])


encoders = {}
if 'gender' in X_train.columns:
    le = LabelEncoder()
    X_train['gender'] = le.fit_transform(X_train['gender'].astype(str))
    X_test['gender'] = le.transform(X_test['gender'].astype(str))
    encoders['gender'] = le


X_train = X_train.fillna(X_train.median(numeric_only=True))
X_test  = X_test.fillna(X_train.median(numeric_only=True))


mi_scores = mutual_info_regression(X_train, y_train, random_state=42)
mi_series = pd.Series(mi_scores, index=X_train.columns)

selected_features = mi_series[mi_series > 0.001].index.tolist()

X_train = X_train[selected_features]
X_test  = X_test[selected_features]

logger.info(f"Features selected: {len(selected_features)}")


models = {
    "LinearRegression": Pipeline([
        ("scaler", StandardScaler()),
        ("model", LinearRegression())
    ]),
    "Ridge": Pipeline([
        ("scaler", StandardScaler()),
        ("model", Ridge(alpha=1.0))
    ]),
    "RandomForest": RandomForestRegressor(
        n_estimators=50, random_state=42, n_jobs=1
    ),
    "GradientBoosting": GradientBoostingRegressor(
        n_estimators=50, random_state=42
    )
}


cv = KFold(n_splits=3, shuffle=True, random_state=42)

results = {}
best_name = ""

with mlflow.start_run(run_name="flight-price-training") as parent_run:
    mlflow.set_tag("project", "voyage-analytics")
    mlflow.set_tag("task", "regression")
    mlflow.log_params(
        {
            "sample_size": int(df.shape[0]),
            "train_rows": int(X_train.shape[0]),
            "test_rows": int(X_test.shape[0]),
            "features_selected": int(len(selected_features)),
            "cv_splits": 3,
            "random_state": 42,
        }
    )

    for name, model in models.items():
        t0 = time.time()

        with mlflow.start_run(run_name=name, nested=True):
            cv_scores = cross_val_score(model, X_train, y_train, cv=cv, scoring='r2', n_jobs=1)

            model.fit(X_train, y_train)

            train_preds = model.predict(X_train)
            test_preds = model.predict(X_test)

            train_r2 = r2_score(y_train, train_preds)
            test_r2 = r2_score(y_test, test_preds)
            mae = mean_absolute_error(y_test, test_preds)
            rmse = np.sqrt(mean_squared_error(y_test, test_preds))
            cv_mean = cv_scores.mean()
            train_time = time.time() - t0

            results[name] = {
                "model": model,
                "train_r2": train_r2,
                "r2": test_r2,
                "mae": mae,
                "rmse": rmse,
                "cv_mean": cv_mean,
                "train_time_sec": train_time,
            }

            mlflow.log_metric("train_r2", train_r2)
            mlflow.log_metric("test_r2", test_r2)
            mlflow.log_metric("mae", mae)
            mlflow.log_metric("rmse", rmse)
            mlflow.log_metric("cv_r2_mean", cv_mean)
            mlflow.log_metric("train_time_sec", train_time)
            mlflow.log_param("model_name", name)

            logger.info(f"{name} | Test R2={results[name]['r2']:.4f}")

    best_name = max(results.items(), key=lambda x: x[1]["r2"])[0]
    final_model = results[best_name]["model"]
    mlflow.log_param("best_model", best_name)
    mlflow.log_metric("best_test_r2", results[best_name]["r2"])
    mlflow.log_metric("best_mae", results[best_name]["mae"])

    joblib.dump(final_model, "models/final_model.pkl")
    joblib.dump(selected_features, "models/features.pkl")
    joblib.dump(encoders, "models/encoders.pkl")
    joblib.dump(target_encode_mappings, "models/target_encodings.pkl")

    mlflow.log_artifact("models/final_model.pkl", artifact_path="local_artifacts")
    mlflow.log_artifact("models/features.pkl", artifact_path="local_artifacts")
    mlflow.log_artifact("models/encoders.pkl", artifact_path="local_artifacts")
    mlflow.log_artifact("models/target_encodings.pkl", artifact_path="local_artifacts")

    model_info = mlflow.sklearn.log_model(
        sk_model=final_model,
        artifact_path="model",
        registered_model_name=MLFLOW_REGISTERED_MODEL_NAME,
    )

    report = {
        "model": best_name,
        "r2": float(results[best_name]["r2"]),
        "mae": float(results[best_name]["mae"]),
        "rmse": float(results[best_name]["rmse"]),
        "mlflow_tracking_uri": MLFLOW_TRACKING_URI,
        "mlflow_experiment": MLFLOW_EXPERIMENT_NAME,
        "mlflow_registered_model": MLFLOW_REGISTERED_MODEL_NAME,
        "mlflow_model_uri": model_info.model_uri,
    }

    with open("reports/report.json", "w") as f:
        json.dump(report, f, indent=2)

    mlflow.log_artifact("reports/report.json")

    logger.info("Best model registered to MLflow model registry name: %s", MLFLOW_REGISTERED_MODEL_NAME)

logger.info(f"Best model: {best_name}")

logger.info("Final model saved successfully with MLflow tracking.")