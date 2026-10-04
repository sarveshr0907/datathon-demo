
# ============================================================
# ROUND 3 — PREDICTION / CHALLENGE
# Model: Next-Hour PM2.5 Prediction
# ============================================================

import os
import glob
import numpy as np
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error


# ============================================================
# 1. PATHS
# ============================================================

BASE_DIR = "/content/drive/MyDrive/Round 3 – Prediction/Round 3 – Prediction"

DATA_DIR = os.path.join(BASE_DIR, "Datas")

PREDICTION_DIR = os.path.join(BASE_DIR, "Predictions")
RESULTS_DIR = os.path.join(BASE_DIR, "Results_Evaluation")

os.makedirs(PREDICTION_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)


# ============================================================
# 2. LOAD ALL CSV FILES
# ============================================================

records = []

for city in ["Chennai", "Delhi", "Mumbai"]:

    city_path = os.path.join(DATA_DIR, city)

    for station in os.listdir(city_path):

        station_path = os.path.join(city_path, station)

        if not os.path.isdir(station_path):
            continue

        csv_files = glob.glob(
            os.path.join(station_path, "*.csv")
        )

        for filepath in csv_files:

            df = pd.read_csv(filepath)

            df["Timestamp"] = pd.to_datetime(
                df["Timestamp"]
            )

            df["City"] = city
            df["Station"] = station

            records.append(df)


data = pd.concat(
    records,
    ignore_index=True
)

data = data.sort_values(
    ["City", "Station", "Timestamp"]
).reset_index(drop=True)


# ============================================================
# 3. CREATE NEXT-HOUR TARGET
# ============================================================

data["Target_Next_Hour"] = (
    data
    .groupby(["City", "Station"])["PM2.5 (µg/m³)"]
    .shift(-1)
)


# ============================================================
# 4. CREATE PM2.5 LAG FEATURES
# ============================================================

for lag in [1, 2, 3, 6, 24]:

    data[f"PM25_lag{lag}"] = (
        data
        .groupby(["City", "Station"])["PM2.5 (µg/m³)"]
        .shift(lag)
    )


# ============================================================
# 5. CREATE TIME FEATURES
# ============================================================

data["Hour"] = data["Timestamp"].dt.hour

data["DayOfWeek"] = (
    data["Timestamp"].dt.dayofweek
)

data["Month"] = (
    data["Timestamp"].dt.month
)


# ============================================================
# 6. FEATURES
# ============================================================

numeric_features = [

    "PM2.5 (µg/m³)",
    "PM10 (µg/m³)",
    "NO (µg/m³)",
    "NO2 (µg/m³)",
    "NOx (ppb)",
    "NH3 (µg/m³)",
    "SO2 (µg/m³)",
    "CO (mg/m³)",
    "Ozone (µg/m³)",

    "AT (°C)",
    "RH (%)",
    "WS (m/s)",
    "WD (deg)",
    "TOT-RF (mm)",
    "SR (W/mt2)",
    "BP (mmHg)",

    "PM25_lag1",
    "PM25_lag2",
    "PM25_lag3",
    "PM25_lag6",
    "PM25_lag24",

    "Hour",
    "DayOfWeek",
    "Month"
]


categorical_features = [
    "City",
    "Station"
]


features = (
    numeric_features
    + categorical_features
)


# ============================================================
# 7. REMOVE ROWS WITHOUT TARGET
# ============================================================

model_data = data.dropna(
    subset=["Target_Next_Hour"]
).copy()


# ============================================================
# 8. CHRONOLOGICAL TRAIN / PUBLIC / PRIVATE SPLIT
# ============================================================

train_data = model_data[
    model_data["Timestamp"] < "2023-01-01"
].copy()


public_data = model_data[
    (model_data["Timestamp"] >= "2023-01-01")
    &
    (model_data["Timestamp"] < "2023-07-01")
].copy()


private_data = model_data[
    model_data["Timestamp"] >= "2023-07-01"
].copy()


X_train = train_data[features]
y_train = train_data["Target_Next_Hour"]

X_public = public_data[features]
y_public = public_data["Target_Next_Hour"]

X_private = private_data[features]
y_private = private_data["Target_Next_Hour"]


# ============================================================
# 9. PREPROCESSING
# ============================================================

numeric_pipeline = Pipeline(
    steps=[
        (
            "imputer",
            SimpleImputer(
                strategy="median"
            )
        )
    ]
)


categorical_pipeline = Pipeline(
    steps=[
        (
            "imputer",
            SimpleImputer(
                strategy="most_frequent"
            )
        ),
        (
            "encoder",
            OneHotEncoder(
                handle_unknown="ignore"
            )
        )
    ]
)


preprocessor = ColumnTransformer(
    transformers=[
        (
            "numeric",
            numeric_pipeline,
            numeric_features
        ),
        (
            "categorical",
            categorical_pipeline,
            categorical_features
        )
    ]
)


# ============================================================
# 10. RANDOM FOREST MODEL
# ============================================================

model = RandomForestRegressor(
    n_estimators=100,
    max_depth=20,
    min_samples_leaf=2,
    random_state=42,
    n_jobs=-1
)


model_pipeline = Pipeline(
    steps=[
        (
            "preprocessor",
            preprocessor
        ),
        (
            "model",
            model
        )
    ]
)


# ============================================================
# 11. TRAIN
# ============================================================

print("Training model...")

model_pipeline.fit(
    X_train,
    y_train
)

print("Training completed.")


# ============================================================
# 12. PREDICTION
# ============================================================

public_predictions = (
    model_pipeline.predict(X_public)
)

private_predictions = (
    model_pipeline.predict(X_private)
)


# ============================================================
# 13. EVALUATION
# ============================================================

public_mae = mean_absolute_error(
    y_public,
    public_predictions
)

public_rmse = np.sqrt(
    mean_squared_error(
        y_public,
        public_predictions
    )
)


private_mae = mean_absolute_error(
    y_private,
    private_predictions
)

private_rmse = np.sqrt(
    mean_squared_error(
        y_private,
        private_predictions
    )
)


print("\nPUBLIC TEST")
print("MAE :", public_mae)
print("RMSE:", public_rmse)


print("\nPRIVATE TEST")
print("MAE :", private_mae)
print("RMSE:", private_rmse)


# ============================================================
# 14. CREATE PREDICTION FILE
# ============================================================

public_output = public_data[
    [
        "Timestamp",
        "City",
        "Station"
    ]
].copy()

public_output["Split"] = "Public"

public_output[
    "Predicted_PM25_next_hour"
] = public_predictions


private_output = private_data[
    [
        "Timestamp",
        "City",
        "Station"
    ]
].copy()

private_output["Split"] = "Private"

private_output[
    "Predicted_PM25_next_hour"
] = private_predictions


prediction_output = pd.concat(
    [
        public_output,
        private_output
    ],
    ignore_index=True
)


prediction_path = os.path.join(
    PREDICTION_DIR,
    "predictions.csv"
)


prediction_output.to_csv(
    prediction_path,
    index=False
)


print(
    "\nPredictions saved to:",
    prediction_path
)


# ============================================================
# 15. SAVE RESULTS
# ============================================================

results = pd.DataFrame(
    {
        "Dataset": [
            "Public Test",
            "Private Test"
        ],

        "MAE": [
            public_mae,
            private_mae
        ],

        "RMSE": [
            public_rmse,
            private_rmse
        ]
    }
)


results_path = os.path.join(
    RESULTS_DIR,
    "model_results.csv"
)


results.to_csv(
    results_path,
    index=False
)


print(
    "Results saved to:",
    results_path
)
