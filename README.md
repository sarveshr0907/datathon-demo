# 🏛️ College Datathon 2026 – Air Quality Analysis & Prediction

This repository contains the complete end-to-end solution developed for the College Datathon 2026.

The project demonstrates a four-round workflow covering data auditing, statistical investigation, machine-learning prediction, and final solution development using air-quality and meteorological data from Chennai, Delhi and Mumbai.

---

## 🎯 Project Objective

The project investigates air-quality patterns and develops a machine-learning model to predict **next-hour PM2.5 concentration** using historical air-quality, meteorological and time-based information.

---

## 📂 Repository Structure

### `data/`
Contains the raw and cleaned datasets and the project data dictionary.

### `Round 1 – Data Audit/`
Contains:
- Data understanding
- Data-quality checks
- Missing-value analysis
- Outlier analysis
- City/year observations
- Audit Python code
- Supporting graphs and CSV outputs

### `Round 2 – Statistical Investigation/`
Contains:
- Research question
- Hypotheses
- Statistical methodology
- Correlation-analysis Python code

### `Round 3 – Prediction/`
Contains the complete prediction pipeline:
- Input data
- Model methodology
- Random Forest model code
- Predictions
- Actual vs predicted graph
- Prediction-error distribution
- Public/private performance comparison
- Evaluation results

### `Round 4 – Final Solution/`
Contains the final integrated solution, practical applications, limitations and future improvements.

### `AI Usage/`
Contains documentation of AI tools used during project development and verification.

---

## 📊 Dataset

The dataset contains hourly air-quality and meteorological observations from:

- **Chennai**
- **Delhi**
- **Mumbai**

### Dataset Coverage

- Monitoring stations: **9**
- Years: **2021–2023**
- Source CSV files: **27**
- Total observations: **236,520**

Important variables include PM2.5, PM10, NO, NO2, NOx, NH3, SO2, CO, Ozone, temperature, relative humidity, wind speed, rainfall, solar radiation and pressure.

---

## 🔎 Round 1 – Data Audit

The first round focuses on understanding the dataset and identifying data-quality issues before further analysis.

Key activities include:

- Dataset structure and variable identification
- Missing-value analysis
- Duplicate detection
- Outlier detection
- City and station comparison
- Data cleaning and preparation

---

## 📈 Round 2 – Statistical Investigation

### Research Question

How are temperature, relative humidity and solar radiation associated with ground-level ozone concentration across Chennai, Delhi and Mumbai?

### Variables

**Dependent variable**
- Ozone

**Independent variables**
- Temperature
- Relative humidity
- Solar radiation

Correlation analysis is used to investigate the strength and direction of these relationships.

---

## 🤖 Round 3 – Prediction

### Prediction Task

Predict the **next-hour PM2.5 concentration (µg/m³)**.

### Model

**Random Forest Regressor**

Configuration:

- Trees: 100
- Maximum depth: 20
- Minimum samples per leaf: 2
- Random state: 42

### Features

The model uses:

- Historical air-quality variables
- Meteorological variables
- Historical PM2.5 lag values
- Hour, day of week and month
- City and station information

### Time-Based Evaluation

The data was split chronologically:

| Period | Date Range |
|---|---|
| Training | 2021-01-01 to 2022-12-31 |
| Public Test | 2023-01-01 to 2023-06-30 |
| Private Test | 2023-07-01 to 2023-12-31 |

### Prediction Performance

| Metric | Public Test | Private Test |
|---|---:|---:|
| Observations | 36,082 | 30,517 |
| MAE | 17.995 µg/m³ | **19.639 µg/m³** |
| RMSE | 31.142 µg/m³ | **38.215 µg/m³** |

The private test represents a later unseen period and provides a more realistic estimate of future prediction performance.

---

## 💡 Round 4 – Final Solution

The final solution integrates the results from all previous rounds into an end-to-end workflow:

**Data Audit → Statistical Investigation → Prediction → Evaluation → Practical Application**

Potential applications include:

- Short-term air-quality forecasting
- Early identification of rising PM2.5 levels
- Air-quality monitoring
- Data-driven environmental decision-making

---

## ⚠️ Limitations

- Prediction performance may vary across cities and stations.
- Missing and repeated source records can affect analysis.
- Historical data may not represent unusual future events.
- Further model tuning and validation may improve performance.

---

## 🚀 Future Improvements

- Compare additional machine-learning models.
- Perform systematic hyperparameter tuning.
- Add more historical and meteorological features.
- Evaluate performance separately for each city and station.
- Develop a real-time air-quality prediction dashboard.

---

## 👥 Team & Workflow

- **Event:** College Datathon 2026
- **Project Type:** End-to-end air-quality analysis and prediction
- **Workflow:** Data Audit → Statistical Investigation → Prediction → Final Solution

---

## 📌 Note

This repository represents a college datathon demonstration and documents the complete workflow, analysis, prediction methodology and evaluation results used during the dry run.
