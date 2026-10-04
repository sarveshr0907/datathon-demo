import os
import zipfile
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="whitegrid")

print("=" * 60)
print("STEP 1: AUTO-EXTRACTING & PARSING CITY ZIPS")
print("=" * 60)

root_dir = Path(r'C:\Sarvesh R\DGVC\Datathon Dataset')
extract_dir = root_dir / 'extracted_cities'
extract_dir.mkdir(exist_ok=True)

for city_name in ['Chennai', 'Delhi', 'Mumbai']:
    zip_path = root_dir / f"{city_name}.zip"
    city_extract_path = extract_dir / city_name

    if zip_path.exists() and not city_extract_path.exists():
        print(f"Extracting {city_name}.zip...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(city_extract_path)

all_data = []

# Safely walk through extracted folders and find all .csv files
for csv_file in extract_dir.rglob('*.csv'):
    try:
        # Skip hidden or temporary files if any exist
        if csv_file.name.startswith('.'):
            continue

        temp_df = pd.read_csv(csv_file, low_memory=False)

        # Extract City and Station from parent directory structure
        # Structure is usually: extracted_cities / City / Station / file.csv
        parts = csv_file.relative_to(extract_dir).parts
        if len(parts) >= 2:
            city_val = parts[0]
            station_val = parts[1]
        else:
            city_val = "Unknown"
            station_val = "Unknown"

        if 'City' not in temp_df.columns:
            temp_df['City'] = city_val
        if 'Station' not in temp_df.columns:
            temp_df['Station'] = station_val

        all_data.append(temp_df)
    except Exception as e:
        print(f"Skipping file due to read error {csv_file.name}: {e}")

if len(all_data) == 0:
    raise ValueError("ERROR: No readable CSV files found inside the extracted folders!")

master_raw_df = pd.concat(all_data, ignore_index=True)
print(f"Combined Raw Dataset Shape: {master_raw_df.shape}")

print("\n" + "=" * 60)
print("STEP 2: DATA CLEANING & DATE DETECTION")
print("=" * 60)

# Auto-detect date/time column safely
date_col = next(
    (col for col in master_raw_df.columns
     if any(k in col.lower() for k in ['date', 'time', 'timestamp'])),
    None
)

if date_col is None:
    raise ValueError(
        f"Could not find any date/time column! Available columns: {list(master_raw_df.columns)}"
    )

print(f"Detected date column: '{date_col}'")

master_raw_df['Date'] = pd.to_datetime(master_raw_df[date_col], errors='coerce')
master_raw_df['Year'] = master_raw_df['Date'].dt.year

# Filter years from 2019 to 2025
df_cleaned = master_raw_df[
    (master_raw_df['Year'] >= 2019) &
    (master_raw_df['Year'] <= 2025)
].copy()

df_cleaned = df_cleaned.drop_duplicates()

# Find numeric columns to treat as metrics/pollutants
numeric_cols = df_cleaned.select_dtypes(include=[np.number]).columns.tolist()
pollutant_cols = [col for col in numeric_cols if col not in ['Year']]

print(f"Detected metric columns: {pollutant_cols}")

for col in pollutant_cols:
    if col in df_cleaned.columns:
        # Fill missing values with city median
        df_cleaned[col] = pd.to_numeric(df_cleaned[col], errors='coerce')
        df_cleaned[col] = df_cleaned[col].fillna(
            df_cleaned.groupby('City')[col].transform('median')
        )
        df_cleaned = df_cleaned[df_cleaned[col] >= 0]

cleaned_filename = 'cleaned_air_quality_demo.csv'
df_cleaned.to_csv(cleaned_filename, index=False)
print(f"Success! Cleaned dataset saved as '{cleaned_filename}'.")

print("\n" + "=" * 60)
print("ROUND 1: DATA AUDIT & ANSWER KEY GENERATION")
print("=" * 60)

print("\n--- [1] MISSING VALUES CHECK ---")
print(df_cleaned.isnull().sum()[df_cleaned.isnull().sum() > 0])

print("\n--- [2] DUPLICATES CHECK ---")
print(f"Remaining duplicates: {df_cleaned.duplicated().sum()}")

print("\n--- [3] OUTLIERS REPORT (Using IQR) ---")
for col in pollutant_cols[:5]:
    Q1 = df_cleaned[col].quantile(0.25)
    Q3 = df_cleaned[col].quantile(0.75)
    IQR = Q3 - Q1
    outliers = df_cleaned[
        (df_cleaned[col] < Q1 - 1.5 * IQR) |
        (df_cleaned[col] > Q3 + 1.5 * IQR)
    ]
    print(f"'{col}': {len(outliers)} outliers detected.")

# Pick a main variable for trend analysis
main_var = next(
    (c for c in ['PM2.5', 'PM10', 'AQI'] if c in df_cleaned.columns),
    pollutant_cols[0] if pollutant_cols else None
)

if main_var:
    pattern_table = df_cleaned.groupby(
        ['City', 'Year']
    )[main_var].mean().unstack()

    print(f"\n--- [4] CITY-WISE & YEAR-WISE PATTERNS (Mean {main_var}) ---")
    print(pattern_table)

    pattern_table.to_csv('answer_key_city_year_patterns.csv')

    plt.figure(figsize=(10, 6))

    # Filter out rows where main_var or Year is NaN before plotting
    plot_df = df_cleaned.dropna(subset=[main_var, 'Year'])

    if not plot_df.empty:
        sns.lineplot(
            data=plot_df,
            x='Year',
            y=main_var,
            hue='City',
            marker='o',
            linewidth=2.5,
            errorbar=None
        )

        plt.title(
            f'Round 1 Audit: Year-wise Trend of {main_var}',
            fontsize=13,
            fontweight='bold'
        )
        plt.xlabel('Year', fontsize=11)
        plt.ylabel(f'Average {main_var}', fontsize=11)
        plt.legend(title='City', loc='best')
        plt.tight_layout()

        graph_filename = 'round1_city_yearly_trend.png'
        plt.savefig(graph_filename, dpi=300)
        plt.close()

        print(f"\n[Saved Graph] '{graph_filename}' generated successfully!")

print("=" * 60)
print("ROUND 1 COMPLETE!")
print("=" * 60)
