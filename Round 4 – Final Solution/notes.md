# Round 4 – Final Solution

## Objective

To combine the findings from data auditing, statistical investigation and prediction into a practical air-quality prediction solution.

## Problem Addressed

Ground-level air pollution varies across cities and over time. Accurate short-term prediction can help identify changing pollution conditions and support timely air-quality monitoring and decision-making.

## Final Solution

The project uses historical air-quality, meteorological and time-based information to predict the **next-hour PM2.5 concentration**.

The solution combines:

1. Data quality auditing
2. Statistical investigation
3. Machine learning prediction
4. Model evaluation

## Key Findings from Previous Rounds

### Round 1 – Data Audit

- Dataset covers Chennai, Delhi and Mumbai.
- 9 monitoring stations are included.
- Data covers 2021–2023.
- Total observations: 236,520.
- Missing values and data-quality issues were identified and documented.

### Round 2 – Statistical Investigation

The analysis investigates the association between ozone concentration and:

- Temperature
- Relative humidity
- Solar radiation

Correlation analysis is used to understand the strength and direction of these relationships.

### Round 3 – Prediction

A **Random Forest Regressor** was used to predict next-hour PM2.5.

Model configuration:

- Trees: 100
- Maximum depth: 20
- Minimum samples per leaf: 2
- Random state: 42

The model uses historical pollution, meteorological, time and station/city information.

## Prediction Performance

| Metric | Public Test | Private Test |
|---|---:|---:|
| MAE | 17.995 µg/m³ | 19.639 µg/m³ |
| RMSE | 31.142 µg/m³ | 38.215 µg/m³ |

The private test represents a later unseen period and therefore provides a more realistic estimate of future prediction performance.

## Practical Use

The proposed solution can support:

- Short-term air-quality forecasting
- Early identification of rising PM2.5 levels
- Air-quality monitoring
- Data-driven environmental decision-making

## Limitations

- Prediction accuracy can vary across cities and time periods.
- Missing and repeated source records can affect analysis.
- The model is based on historical observations and may not capture unusual future events.
- Further tuning and validation could improve prediction performance.

## Future Improvements

- Test additional machine-learning models.
- Perform systematic hyperparameter tuning.
- Add more historical and meteorological features.
- Evaluate performance separately for each city and station.
- Investigate additional methods for handling repeated records.
- Develop a real-time prediction dashboard.

## Conclusion

The project demonstrates an end-to-end workflow from data auditing and statistical investigation to machine-learning prediction.

The Random Forest model achieved a private-test MAE of **19.639 µg/m³** and RMSE of **38.215 µg/m³**, demonstrating its ability to predict next-hour PM2.5 from historical environmental data.
