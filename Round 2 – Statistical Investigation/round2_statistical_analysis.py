import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load cleaned dataset
file_path = "cleaned_air_quality_demo.csv"
df = pd.read_csv(file_path)
print(df.columns.tolist())

# Convert required columns to numeric
columns = [
    "Ozone (µg/m³)",
    "AT (°C)",
    "RH (%)",
    "SR (W/mt2)"
]

for col in columns:
    print("\n", col)
    print(df[col].head(10).tolist())

# Keep only required variables
analysis_df = df[columns].dropna()
print("\nNumber of usable rows:", len(analysis_df))
print("\nSample data:")
print(df[columns].head())

# Calculate correlation matrix
correlation_matrix = analysis_df.corr()

print("\nCorrelation Matrix:")
print(correlation_matrix)

# Save correlation results
correlation_matrix.to_csv("round2_correlation_matrix.csv")

# Create heatmap
plt.figure(figsize=(8, 6))

sns.heatmap(
    correlation_matrix,
    annot=True,
    cmap="coolwarm",
    fmt=".2f",
    linewidths=0.5
)

plt.title("Correlation Between Ozone and Meteorological Variables")
plt.tight_layout()

plt.savefig("round2_correlation_heatmap.png", dpi=300)
plt.show()

print("\nRound 2 analysis completed.")
print("Files created:")
print("- round2_correlation_matrix.csv")
print("- round2_correlation_heatmap.png")