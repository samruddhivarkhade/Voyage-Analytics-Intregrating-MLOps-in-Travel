import pandas as pd
import numpy as np
import logging
import os
import json
import joblib
import time

from sklearn.model_selection import train_test_split, KFold, cross_val_score, RandomizedSearchCV
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.feature_selection import mutual_info_regression

from sklearn.linear_model import LinearRegression, Ridge
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, VotingRegressor

from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from scipy.stats import randint, uniform

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

os.makedirs("models", exist_ok=True)
os.makedirs("reports", exist_ok=True)

flights = pd.read_csv("data/flights.csv")
users   = pd.read_csv("data/users.csv")

df = pd.merge(flights, users, left_on="userCode", right_on="code")
logger.info(f"Data loaded: {df.shape}")

df['date'] = pd.to_datetime(df['date'], errors='coerce')
df['day_of_week'] = df['date'].dt.dayofweek
df['month'] = df['date'].dt.month
df['is_weekend'] = (df['day_of_week'] >= 5).astype(int)
df['route'] = df['from'].astype(str) + "_" + df['to'].astype(str)

df['age_group'] = pd.cut(df['age'], bins=[0,17,25,35,50,65,120], labels=[0,1,2,3,4,5]).astype(float)

TARGET = "price"

X = df.drop(columns=[TARGET])
y = df[TARGET]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

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
for col in ['gender']:
    if col in X_train.columns:
        le = LabelEncoder()
        X_train[col] = le.fit_transform(X_train[col].astype(str))
        X_test[col] = le.transform(X_test[col].astype(str))
        encoders[col] = le

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
    "RandomForest": RandomForestRegressor(n_estimators=200, random_state=42, n_jobs=-1),
    "GradientBoosting": GradientBoostingRegressor(n_estimators=200, random_state=42)
}

cv = KFold(n_splits=5, shuffle=True, random_state=42)

results = {}

for name, model in models.items():
    t0 = time.time()
    cv_scores = cross_val_score(model, X_train, y_train, cv=cv, scoring='r2', n_jobs=-1)
    model.fit(X_train, y_train)
    
    # Train predictions and metrics
    train_preds = model.predict(X_train)
    train_r2 = r2_score(y_train, train_preds)
    train_mae = mean_absolute_error(y_train, train_preds)
    train_rmse = np.sqrt(mean_squared_error(y_train, train_preds))
    
    # Test predictions and metrics
    preds = model.predict(X_test)
    test_r2 = r2_score(y_test, preds)
    test_mae = mean_absolute_error(y_test, preds)
    test_rmse = np.sqrt(mean_squared_error(y_test, preds))

    results[name] = {
        "model": model,
        "train_r2": train_r2,
        "train_mae": train_mae,
        "train_rmse": train_rmse,
        "r2": test_r2,
        "mae": test_mae,
        "rmse": test_rmse,
        "cv_mean": cv_scores.mean(),
        "cv_std": cv_scores.std()
    }

    logger.info(f"{name} | Train R2={train_r2:.4f} | Test R2={test_r2:.4f} | Train MAE={train_mae:.2f} | Test MAE={test_mae:.2f} | CV={cv_scores.mean():.4f}±{cv_scores.std():.4f}")

best_name = max(results.items(), key=lambda x: x[1]["r2"])[0]
final_model = results[best_name]["model"]
best_r2 = results[best_name]["r2"]

logger.info(f"Best model: {best_name} with Test R2={best_r2:.4f}")
final_name = best_name

joblib.dump(final_model, "models/final_model.pkl")
joblib.dump(selected_features, "models/features.pkl")
joblib.dump(encoders, "models/encoders.pkl")
joblib.dump(target_encode_mappings, "models/target_encodings.pkl")

best_mae = results[best_name]["mae"]
report = {
    "final_model": final_name,
    "r2": float(best_r2),
    "mae": float(best_mae),
    "features": selected_features
}

with open("reports/report.json", "w") as f:
    json.dump(report, f, indent=2)

logger.info(f"Final model saved: {final_name}")