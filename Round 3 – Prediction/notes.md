# Round 3 – Prediction

## Prediction Task

Predict the **next-hour PM2.5 concentration (µg/m³)** using historical air-quality, meteorological and time-based features.

## Dataset

- Cities: Chennai, Delhi, Mumbai
- Stations: 9
- Years: 2021–2023
- Source CSV files: 27
- Total observations: 236,520

## Features Used

- Air-quality variables: PM2.5, PM10, NO, NO2, NOx, NH3, SO2, CO, Ozone
- Meteorological variables: AT, RH, WS, WD, TOT-RF, SR, BP
- Historical PM2.5 lags: 1h, 2h, 3h, 6h, 24h
- Time variables: Hour, Day of Week, Month
- Categorical variables: City, Station

## Model

**Random Forest Regressor**

- Trees: 100
- Maximum depth: 20
- Minimum samples per leaf: 2
- Random state: 42

Random Forest was selected because it can capture nonlinear relationships between air-quality, meteorological and time-based features.

## Train/Test Design

A chronological split was used to avoid future information leaking into training.

- Training: 2021-01-01 to 2022-12-31
- Public test: 2023-01-01 to 2023-06-30
- Private test: 2023-07-01 to 2023-12-31

## Evaluation Results

| Metric | Public Test | Private Test |
|---|---:|---:|
| Observations | 36,082 | 30,517 |
| MAE | 17.995 µg/m³ | 19.639 µg/m³ |
| RMSE | 31.142 µg/m³ | 38.215 µg/m³ |

## Interpretation

MAE represents the average absolute difference between predicted and actual PM2.5 concentration.

RMSE gives greater penalty to larger prediction errors.

The private test represents a later unseen period and therefore provides a more realistic estimate of future prediction performance.

## Missing Value Handling

- Numerical missing values: median imputation
- Categorical missing values: most-frequent imputation
- Imputation was performed within the machine-learning pipeline.

## Output

The prediction output contains:

- Timestamp
- City
- Station
- Split
- Predicted next-hour PM2.5

## Data Quality Note

The preliminary audit identified repeated source records across several station files. The supplied station-year files were retained and the duplication was documented rather than silently modifying the source data.
