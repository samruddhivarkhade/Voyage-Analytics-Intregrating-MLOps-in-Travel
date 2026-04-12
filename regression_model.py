"""
╔══════════════════════════════════════════════════════════════╗
║        FLIGHT PRICE PREDICTION — ADVANCED ML PIPELINE        ║
║  Feature Engineering + Multi-Model Training + HPO Tuning     ║
╚══════════════════════════════════════════════════════════════╝
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, KFold, RandomizedSearchCV
from sklearn.preprocessing import LabelEncoder, StandardScaler, PolynomialFeatures
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet
from sklearn.ensemble import (
    RandomForestRegressor, GradientBoostingRegressor,
    ExtraTreesRegressor, AdaBoostRegressor, VotingRegressor
)
from sklearn.tree import DecisionTreeRegressor
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from sklearn.pipeline import Pipeline
from sklearn.feature_selection import SelectFromModel, mutual_info_regression
import joblib
import warnings
import os
import json
import time
from scipy.stats import randint, uniform

warnings.filterwarnings('ignore')

try:
    from xgboost import XGBRegressor
    HAS_XGB = True
except ImportError:
    HAS_XGB = False
    print("⚠️  XGBoost not installed. Skipping XGBRegressor.")

try:
    from lightgbm import LGBMRegressor
    HAS_LGBM = True
except ImportError:
    HAS_LGBM = False
    print("⚠️  LightGBM not installed. Skipping LGBMRegressor.")

os.makedirs("models", exist_ok=True)
os.makedirs("reports", exist_ok=True)

# ──────────────────────────────────────────────────────────────
# 1. LOAD & MERGE
# ──────────────────────────────────────────────────────────────
print("\n" + "═"*60)
print("  STEP 1 — Loading & Merging Datasets")
print("═"*60)

flights = pd.read_csv("data/flights.csv")
users   = pd.read_csv("data/users.csv")

flight_data = pd.merge(flights, users, left_on="userCode", right_on="code")
print(f"  ✔ Merged shape : {flight_data.shape}")
print(f"  ✔ Columns      : {list(flight_data.columns)}")

# ──────────────────────────────────────────────────────────────
# 2. FEATURE ENGINEERING
# ──────────────────────────────────────────────────────────────
print("\n" + "═"*60)
print("  STEP 2 — Feature Engineering")
print("═"*60)

df = flight_data.copy()

# ── 2a. Date features ──────────────────────────────────────────
if 'date' in df.columns:
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df['day_of_week']   = df['date'].dt.dayofweek          # 0=Mon … 6=Sun
    df['month']         = df['date'].dt.month
    df['day_of_month']  = df['date'].dt.day
    df['is_weekend']    = (df['day_of_week'] >= 5).astype(int)
    df['quarter']       = df['date'].dt.quarter
    # Peak travel months: June–Aug (summer) and Dec (holiday)
    df['is_peak_season']= df['month'].isin([6, 7, 8, 12]).astype(int)
    print("  ✔ Date features       : day_of_week, month, day_of_month, is_weekend, quarter, is_peak_season")

# ── 2b. Age features ──────────────────────────────────────────
if 'age' in df.columns:
    df['age_group'] = pd.cut(
        df['age'],
        bins=[0, 17, 25, 35, 50, 65, 120],
        labels=[0, 1, 2, 3, 4, 5]
    ).astype(float)
    df['is_senior']  = (df['age'] >= 60).astype(int)
    df['is_student'] = (df['age'] <= 25).astype(int)
    print("  ✔ Age features        : age_group, is_senior, is_student")

# ── 2c. Route / geography features ────────────────────────────
if 'from' in df.columns and 'to' in df.columns:
    df['route'] = df['from'].astype(str) + "_" + df['to'].astype(str)

    # Route popularity (frequency encoding)
    route_freq  = df['route'].value_counts().to_dict()
    df['route_popularity'] = df['route'].map(route_freq)

    # Per-route mean price (target encoding with smoothing)
    global_mean  = df['price'].mean()
    route_stats  = df.groupby('route')['price'].agg(['mean', 'count'])
    smooth_k     = 10  # smoothing factor
    route_stats['smooth_mean'] = (
        (route_stats['mean'] * route_stats['count'] + global_mean * smooth_k)
        / (route_stats['count'] + smooth_k)
    )
    df['route_mean_price'] = df['route'].map(route_stats['smooth_mean'])
    print("  ✔ Route features      : route_popularity, route_mean_price")

# ── 2d. Agency features ───────────────────────────────────────
if 'agency' in df.columns:
    agency_freq = df['agency'].value_counts().to_dict()
    df['agency_popularity'] = df['agency'].map(agency_freq)

    agency_mean = df.groupby('agency')['price'].mean().to_dict()
    df['agency_mean_price'] = df['agency'].map(agency_mean)
    print("  ✔ Agency features     : agency_popularity, agency_mean_price")

# ── 2e. Flight-type premium ───────────────────────────────────
if 'flightType' in df.columns:
    ft_mean = df.groupby('flightType')['price'].mean().to_dict()
    df['flightType_mean_price'] = df['flightType'].map(ft_mean)
    print("  ✔ FlightType feature  : flightType_mean_price")

# ── 2f. Interaction features ──────────────────────────────────
numeric_pairs = []
if 'age' in df.columns and 'flightType' in df.columns:
    # We'll create numerical interactions after encoding
    numeric_pairs.append(('age', 'flightType_mean_price'))

# ──────────────────────────────────────────────────────────────
# 3. ENCODE CATEGORICALS
# ──────────────────────────────────────────────────────────────
print("\n" + "═"*60)
print("  STEP 3 — Encoding Categorical Columns")
print("═"*60)

drop_cols = [
    'travelCode', 'userCode', 'code',
    'name', 'company', 'date', 'from', 'to', 'route'
]
df = df.drop([c for c in drop_cols if c in df.columns], axis=1)

encoders = {}
for col in ['flightType', 'agency', 'gender']:
    if col in df.columns:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col].astype(str))
        encoders[col] = le
        print(f"  ✔ Encoded: {col}")

# ── 2f (cont) — Numerical interaction features ─────────────────
if 'age' in df.columns and 'agency_mean_price' in df.columns:
    df['age_x_agency_price'] = df['age'] * df['agency_mean_price']
    print("  ✔ Interaction         : age × agency_mean_price")

if 'is_peak_season' in df.columns and 'flightType' in df.columns:
    df['peak_x_flightType'] = df['is_peak_season'] * df['flightType']
    print("  ✔ Interaction         : is_peak_season × flightType")

# ── 2g. Log-transform skewed numerics ─────────────────────────
for col in ['price']:
    if col in df.columns:
        df[f'log_{col}'] = np.log1p(df[col])

# ──────────────────────────────────────────────────────────────
# 4. HANDLE MISSING VALUES
# ──────────────────────────────────────────────────────────────
print("\n" + "═"*60)
print("  STEP 4 — Handling Missing Values")
print("═"*60)

missing_before = df.isnull().sum().sum()
df = df.fillna(df.median(numeric_only=True))
missing_after = df.isnull().sum().sum()
print(f"  ✔ Missing values: {missing_before} → {missing_after}")

# ──────────────────────────────────────────────────────────────
# 5. OUTLIER REMOVAL (IQR capping)
# ──────────────────────────────────────────────────────────────
print("\n" + "═"*60)
print("  STEP 5 — Outlier Capping (IQR Method)")
print("═"*60)

shape_before = df.shape[0]
Q1 = df['price'].quantile(0.01)
Q3 = df['price'].quantile(0.99)
df = df[(df['price'] >= Q1) & (df['price'] <= Q3)]
print(f"  ✔ Rows: {shape_before} → {df.shape[0]} (removed extreme price outliers)")

# ──────────────────────────────────────────────────────────────
# 6. FEATURE SELECTION
# ──────────────────────────────────────────────────────────────
print("\n" + "═"*60)
print("  STEP 6 — Feature Selection (Mutual Information)")
print("═"*60)

TARGET = 'price'
X = df.drop([TARGET, 'log_price'], axis=1, errors='ignore')
y = df[TARGET]

# Mutual information to rank features
mi_scores = mutual_info_regression(X.fillna(0), y, random_state=42)
mi_series = pd.Series(mi_scores, index=X.columns).sort_values(ascending=False)
print("\n  Feature Importance (Mutual Information):")
for feat, score in mi_series.items():
    bar = "█" * int(score * 30)
    print(f"    {feat:<30} {score:.4f}  {bar}")

# Drop near-zero MI features
keep_features = mi_series[mi_series > 0.001].index.tolist()
X = X[keep_features]
print(f"\n  ✔ Features kept: {len(keep_features)} / {len(mi_series)}")
print(f"  ✔ Selected: {keep_features}")

# ──────────────────────────────────────────────────────────────
# 7. TRAIN / TEST SPLIT
# ──────────────────────────────────────────────────────────────
print("\n" + "═"*60)
print("  STEP 7 — Train/Test Split (80/20)")
print("═"*60)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
print(f"  ✔ Train size: {X_train.shape}")
print(f"  ✔ Test  size: {X_test.shape}")

scaler = StandardScaler()
X_train_sc = scaler.fit_transform(X_train)
X_test_sc  = scaler.transform(X_test)

# ──────────────────────────────────────────────────────────────
# 8. MULTI-MODEL BENCHMARK
# ──────────────────────────────────────────────────────────────
print("\n" + "═"*60)
print("  STEP 8 — Multi-Model Benchmark (Cross-Validation)")
print("═"*60)

cv = KFold(n_splits=5, shuffle=True, random_state=42)

base_models = {
    "LinearRegression"   : (LinearRegression(), False),
    "Ridge"              : (Ridge(alpha=1.0), False),
    "Lasso"              : (Lasso(alpha=0.1), False),
    "ElasticNet"         : (ElasticNet(alpha=0.1, l1_ratio=0.5), False),
    "DecisionTree"       : (DecisionTreeRegressor(random_state=42), False),
    "KNeighbors"         : (KNeighborsRegressor(n_neighbors=10), True),
    "RandomForest"       : (RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1), False),
    "ExtraTrees"         : (ExtraTreesRegressor(n_estimators=100, random_state=42, n_jobs=-1), False),
    "GradientBoosting"   : (GradientBoostingRegressor(n_estimators=100, random_state=42), False),
    "AdaBoost"           : (AdaBoostRegressor(n_estimators=100, random_state=42), False),
}

if HAS_XGB:
    base_models["XGBoost"] = (XGBRegressor(n_estimators=100, random_state=42,
                                            verbosity=0, n_jobs=-1), False)
if HAS_LGBM:
    base_models["LightGBM"] = (LGBMRegressor(n_estimators=100, random_state=42,
                                              verbose=-1, n_jobs=-1), False)

results = {}

for name, (model, use_scaled) in base_models.items():
    t0   = time.time()
    Xtr  = X_train_sc if use_scaled else X_train
    Xte  = X_test_sc  if use_scaled else X_test

    cv_r2 = cross_val_score(model, Xtr, y_train, cv=cv, scoring='r2', n_jobs=-1)

    model.fit(Xtr, y_train)
    preds = model.predict(Xte)

    r2  = r2_score(y_test, preds)
    mae = mean_absolute_error(y_test, preds)
    rmse= np.sqrt(mean_squared_error(y_test, preds))
    elapsed = time.time() - t0

    results[name] = {
        "model"       : model,
        "use_scaled"  : use_scaled,
        "cv_r2_mean"  : cv_r2.mean(),
        "cv_r2_std"   : cv_r2.std(),
        "test_r2"     : r2,
        "mae"         : mae,
        "rmse"        : rmse,
        "train_time"  : elapsed,
    }

    status = "✅" if r2 >= 0.85 else "⚠️ " if r2 >= 0.70 else "❌"
    print(f"  {status}  {name:<22}  R²={r2:.4f}  MAE={mae:>8.2f}  CV={cv_r2.mean():.4f}±{cv_r2.std():.4f}  ({elapsed:.1f}s)")

# ──────────────────────────────────────────────────────────────
# 9. HYPERPARAMETER TUNING — Best model(s)
# ──────────────────────────────────────────────────────────────
print("\n" + "═"*60)
print("  STEP 9 — Hyperparameter Tuning (RandomizedSearchCV)")
print("═"*60)

# Sort by test R²; pick top model(s)
sorted_results = sorted(results.items(), key=lambda x: x[1]['test_r2'], reverse=True)
best_name, best_info = sorted_results[0]
print(f"\n  Top model to tune: {best_name}  (R²={best_info['test_r2']:.4f})")

param_grids = {
    "RandomForest": {
        "n_estimators"      : randint(100, 600),
        "max_depth"         : [None, 10, 20, 30, 40],
        "min_samples_split" : randint(2, 10),
        "min_samples_leaf"  : randint(1, 5),
        "max_features"      : ["sqrt", "log2", 0.5, 0.7],
    },
    "GradientBoosting": {
        "n_estimators"  : randint(100, 500),
        "learning_rate" : uniform(0.01, 0.2),
        "max_depth"     : randint(3, 10),
        "subsample"     : uniform(0.6, 0.4),
        "min_samples_split": randint(2, 10),
    },
    "ExtraTrees": {
        "n_estimators"      : randint(100, 600),
        "max_depth"         : [None, 10, 20, 30],
        "min_samples_split" : randint(2, 10),
        "min_samples_leaf"  : randint(1, 4),
    },
    "XGBoost": {
        "n_estimators"  : randint(100, 600),
        "learning_rate" : uniform(0.01, 0.2),
        "max_depth"     : randint(3, 10),
        "subsample"     : uniform(0.6, 0.4),
        "colsample_bytree": uniform(0.5, 0.5),
        "gamma"         : uniform(0, 0.3),
        "reg_alpha"     : uniform(0, 1),
        "reg_lambda"    : uniform(0.5, 2),
    },
    "LightGBM": {
        "n_estimators"  : randint(100, 600),
        "learning_rate" : uniform(0.01, 0.2),
        "num_leaves"    : randint(20, 150),
        "max_depth"     : randint(3, 12),
        "subsample"     : uniform(0.6, 0.4),
        "colsample_bytree": uniform(0.5, 0.5),
        "reg_alpha"     : uniform(0, 1),
        "reg_lambda"    : uniform(0, 1),
    },
}

# Default to GradientBoosting if best model has no param grid
tune_name = best_name if best_name in param_grids else "GradientBoosting"
tune_model_base, tune_scaled = base_models[tune_name]

Xtr = X_train_sc if tune_scaled else X_train
Xte = X_test_sc  if tune_scaled else X_test

print(f"  Tuning: {tune_name} with RandomizedSearchCV (n_iter=40, cv=5)...")

rscv = RandomizedSearchCV(
    estimator=tune_model_base,
    param_distributions=param_grids[tune_name],
    n_iter=40,
    cv=cv,
    scoring='r2',
    n_jobs=-1,
    random_state=42,
    verbose=1,
)
rscv.fit(Xtr, y_train)

tuned_model  = rscv.best_estimator_
tuned_preds  = tuned_model.predict(Xte)
tuned_r2     = r2_score(y_test, tuned_preds)
tuned_mae    = mean_absolute_error(y_test, tuned_preds)
tuned_rmse   = np.sqrt(mean_squared_error(y_test, tuned_preds))

print(f"\n  Best params : {rscv.best_params_}")
print(f"  Best CV R²  : {rscv.best_score_:.4f}")
print(f"  Test R²     : {tuned_r2:.4f}")
print(f"  Test MAE    : {tuned_mae:.2f}")
print(f"  Test RMSE   : {tuned_rmse:.2f}")

results[f"{tune_name}_Tuned"] = {
    "model"      : tuned_model,
    "use_scaled" : tune_scaled,
    "cv_r2_mean" : rscv.best_score_,
    "cv_r2_std"  : 0.0,
    "test_r2"    : tuned_r2,
    "mae"        : tuned_mae,
    "rmse"       : tuned_rmse,
    "best_params": rscv.best_params_,
}

# ──────────────────────────────────────────────────────────────
# 10. ENSEMBLE / STACKING
# ──────────────────────────────────────────────────────────────
print("\n" + "═"*60)
print("  STEP 10 — Ensemble (Weighted Voting of Top-3 Models)")
print("═"*60)

top3 = sorted_results[:3]
estimators = []
for nm, inf in top3:
    Xfit = X_train_sc if inf["use_scaled"] else X_train
    inf["model"].fit(Xfit, y_train)
    estimators.append((nm, inf["model"]))
    print(f"  ✔ Included: {nm}")

# Voting Regressor (simple average — no scaling mismatch)
# We re-train each estimator on X_train (unscaled) in a fresh clone
from sklearn.base import clone
ensemble_estimators = []
for nm, inf in top3:
    m = clone(inf["model"])
    m.fit(X_train, y_train)
    ensemble_estimators.append((nm, m))

ensemble = VotingRegressor(estimators=ensemble_estimators)
ensemble.fit(X_train, y_train)
ens_preds = ensemble.predict(X_test)
ens_r2    = r2_score(y_test, ens_preds)
ens_mae   = mean_absolute_error(y_test, ens_preds)
ens_rmse  = np.sqrt(mean_squared_error(y_test, ens_preds))

print(f"\n  Ensemble R²   : {ens_r2:.4f}")
print(f"  Ensemble MAE  : {ens_mae:.2f}")
print(f"  Ensemble RMSE : {ens_rmse:.2f}")

results["Ensemble_Top3"] = {
    "model"     : ensemble,
    "use_scaled": False,
    "cv_r2_mean": ens_r2,
    "cv_r2_std" : 0.0,
    "test_r2"   : ens_r2,
    "mae"        : ens_mae,
    "rmse"       : ens_rmse,
}

# ──────────────────────────────────────────────────────────────
# 11. FINAL LEADERBOARD
# ──────────────────────────────────────────────────────────────
print("\n" + "═"*60)
print("  STEP 11 — Final Leaderboard")
print("═"*60)

sorted_final = sorted(results.items(), key=lambda x: x[1]['test_r2'], reverse=True)

print(f"\n  {'Rank':<5} {'Model':<28} {'Test R²':>9} {'MAE':>10} {'RMSE':>10}  {'Target'}")
print("  " + "─"*72)
for rank, (nm, inf) in enumerate(sorted_final, 1):
    r2   = inf['test_r2']
    flag = "✅ ACHIEVED" if r2 >= 0.85 else ("⚠️  Close" if r2 >= 0.75 else "❌")
    print(f"  {rank:<5} {nm:<28} {r2:>9.4f} {inf['mae']:>10.2f} {inf['rmse']:>10.2f}  {flag}")

# ──────────────────────────────────────────────────────────────
# 12. SAVE EVERYTHING
# ──────────────────────────────────────────────────────────────
print("\n" + "═"*60)
print("  STEP 12 — Saving Models & Artifacts")
print("═"*60)

champion_name, champion_info = sorted_final[0]
joblib.dump(champion_info["model"], "models/champion_model.pkl")
joblib.dump(tuned_model,             "models/tuned_model.pkl")
joblib.dump(scaler,                  "models/scaler.pkl")
joblib.dump(encoders,                "models/encoders.pkl")
joblib.dump(keep_features,           "models/selected_features.pkl")

# Save leaderboard as JSON report
report = {
    "champion"       : champion_name,
    "champion_r2"    : champion_info["test_r2"],
    "target_achieved": champion_info["test_r2"] >= 0.85,
    "leaderboard"    : [
        {
            "rank"     : i+1,
            "model"    : nm,
            "test_r2"  : round(inf["test_r2"], 4),
            "mae"      : round(inf["mae"], 2),
            "rmse"     : round(inf["rmse"], 2),
            "cv_r2"    : round(inf.get("cv_r2_mean", 0), 4),
        }
        for i, (nm, inf) in enumerate(sorted_final)
    ],
    "features_used"  : keep_features,
    "tuned_model"    : tune_name,
    "best_params"    : {str(k): str(v) for k, v in rscv.best_params_.items()},
}

with open("reports/ml_report.json", "w") as f:
    json.dump(report, f, indent=2)

print(f"  ✔ Champion model saved → models/champion_model.pkl")
print(f"  ✔ Tuned model saved    → models/tuned_model.pkl")
print(f"  ✔ Scaler saved         → models/scaler.pkl")
print(f"  ✔ Encoders saved       → models/encoders.pkl")
print(f"  ✔ Features saved       → models/selected_features.pkl")
print(f"  ✔ Report saved         → reports/ml_report.json")

print("\n" + "═"*60)
print(f"  🏆  CHAMPION  : {champion_name}")
print(f"  📊  TEST R²   : {champion_info['test_r2']:.4f}  "
      f"({'✅ ≥ 85% target achieved!' if champion_info['test_r2'] >= 0.85 else '⚠️  below 85% — consider more data or deeper tuning'})")
print(f"  📉  MAE       : {champion_info['mae']:.2f}")
print(f"  📉  RMSE      : {champion_info['rmse']:.2f}")
print("═"*60 + "\n")