#!/usr/bin/env python3
"""
Task 2: Exploratory Data Analysis
Financial Inclusion in Ethiopia
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

print("=" * 70)
print("TASK 2: EXPLORATORY DATA ANALYSIS")
print("=" * 70)

# Load enriched data
print("\nLOADING ENRICHED DATASET...")
try:
    df = pd.read_csv('../data/processed/ethiopia_fi_enriched.csv')
    print(f"SUCCESS: Loaded {len(df)} records")
except Exception as e:
    print(f"ERROR: {e}")
    print("Using sample data for demonstration")
    df = pd.DataFrame({
        'record_type': ['observation', 'observation', 'observation', 'event', 'observation'],
        'pillar': ['access', 'access', 'usage', None, 'access'],
        'indicator': ['Account Ownership', 'Account Ownership', 'Digital Payment', 'Telebirr Launch', 'Account Ownership Projection'],
        'value_numeric': [14, 22, 9.45, None, 52.5],
        'observation_date': ['2011-12-31', '2014-12-31', '2024-12-31', '2021-05-01', '2025-12-31'],
        'confidence': ['high', 'high', 'high', 'high', 'low']
    })

# Convert dates
df['obs_date'] = pd.to_datetime(df['observation_date'], errors='coerce')

print("\n" + "=" * 70)
print("1. DATASET OVERVIEW")
print("=" * 70)

print("\nRecord Types:")
print(df['record_type'].value_counts())

print("\nPillar Distribution:")
print(df['pillar'].value_counts(dropna=False))

if 'confidence' in df.columns:
    print("\nConfidence Levels:")
    print(df['confidence'].value_counts(dropna=False))

print("\nTemporal Range:")
print(f"Earliest: {df['obs_date'].min().date()}")
print(f"Latest: {df['obs_date'].max().date()}")

print("\n" + "=" * 70)
print("2. ACCESS ANALYSIS - ACCOUNT OWNERSHIP")
print("=" * 70)

# Get account ownership data
acc_mask = df['indicator'].str.contains('Account', case=False, na=False)
acc_data = df[acc_mask & df['value_numeric'].notna()].copy()
acc_data = acc_data.sort_values('obs_date')

if not acc_data.empty:
    print("\nAccount Ownership Trend:")
    for idx, row in acc_data.iterrows():
        year = row['obs_date'].year
        value = row['value_numeric']
        print(f"  {year}: {value}%")
    
    # Calculate growth
    if len(acc_data) > 1:
        print("\nGrowth Analysis:")
        for i in range(1, len(acc_data)):
            prev_year = acc_data.iloc[i-1]['obs_date'].year
            curr_year = acc_data.iloc[i]['obs_date'].year
            prev_val = acc_data.iloc[i-1]['value_numeric']
            curr_val = acc_data.iloc[i]['value_numeric']
            growth_pp = curr_val - prev_val
            years = curr_year - prev_year
            annual_growth = growth_pp / years if years > 0 else growth_pp
            print(f"  {prev_year}-{curr_year}: +{growth_pp:.1f}pp ({annual_growth:.1f}pp per year)")

print("\n" + "=" * 70)
print("3. KEY INSIGHTS")
print("=" * 70)

print("\nKEY FINDINGS:")
print("1. Account ownership grew rapidly from 2011-2021 (+32pp) but slowed to +3pp from 2021-2024")
print("2. Digital payment adoption (9.45%) lags far behind account ownership (49%)")
print("3. Major events: Telebirr launch (2021), M-Pesa entry (2023)")
print("4. Data limitations: Sparse time series, limited disaggregation")
print("5. Forecasting challenge: Recent slowdown creates uncertainty")

# Create simple visualization
plt.figure(figsize=(10, 6))
if not acc_data.empty:
    plt.plot(acc_data['obs_date'].dt.year, acc_data['value_numeric'], 'o-', linewidth=2, markersize=8)
    plt.title('Account Ownership in Ethiopia', fontsize=14, fontweight='bold')
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Account Ownership (%)', fontsize=12)
    plt.grid(True, alpha=0.3)
    plt.savefig('../reports/figures/eda_simple.png', dpi=300)
    print("\nVisualization saved: ../reports/figures/eda_simple.png")

print("\n" + "=" * 70)
print("TASK 2 COMPLETED")
print("=" * 70)
