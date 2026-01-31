#!/usr/bin/env python3
"""
Task 1: Data Exploration and Enrichment
Financial Inclusion Forecasting for Ethiopia
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

print("=" * 60)
print("TASK 1: DATA EXPLORATION AND ENRICHMENT")
print("=" * 60)

# Load data
print("\nLoading datasets...")
df_unified = pd.read_csv('../data/raw/ethiopia_fi_unified_data.csv')
df_ref = pd.read_csv('../data/raw/reference_codes.csv')

print(f"✓ Unified data: {df_unified.shape[0]} rows, {df_unified.shape[1]} columns")
print(f"✓ Reference codes: {df_ref.shape[0]} rows")

# Basic exploration
print("\nBASIC EXPLORATION")
print("-" * 40)
print("Columns:", df_unified.columns.tolist())
print("\nRecord types:")
print(df_unified['record_type'].value_counts())

# Convert dates
df_unified['observation_date'] = pd.to_datetime(df_unified['observation_date'])
df_unified['collection_date'] = pd.to_datetime(df_unified['collection_date'])

# Show account ownership trend
print("\nACCOUNT OWNERSHIP TREND (2011-2024)")
print("-" * 40)
acc_data = df_unified[df_unified['indicator_code'] == 'ACC_OWNERSHIP']
for _, row in acc_data.iterrows():
    print(f"{row['observation_date'].year}: {row['value_numeric']}%")

# Create simple visualization
plt.figure(figsize=(10, 6))
years = acc_data['observation_date'].dt.year
values = acc_data['value_numeric']
plt.plot(years, values, 'o-', linewidth=2, markersize=8)
plt.title('Account Ownership in Ethiopia (2011-2024)', fontsize=14, fontweight='bold')
plt.xlabel('Year', fontsize=12)
plt.ylabel('Account Ownership (%)', fontsize=12)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('../reports/figures/account_trend.png', dpi=300)
print("\n✓ Chart saved to: ../reports/figures/account_trend.png")

# Data enrichment
print("\nDATA ENRICHMENT")
print("-" * 40)

# Add new observations
new_data = [
    {'record_type': 'observation', 'pillar': 'access', 'indicator': 'Account Ownership', 
     'indicator_code': 'ACC_OWNERSHIP', 'value_numeric': 52.5, 
     'observation_date': '2025-12-31', 'source_name': 'Projection', 
     'confidence': 'low', 'notes': 'Projected growth'},
    
    {'record_type': 'observation', 'pillar': 'infrastructure', 'indicator': 'Mobile Penetration',
     'indicator_code': 'MOBILE_PENETRATION', 'value_numeric': 45.2,
     'observation_date': '2024-12-31', 'source_name': 'World Bank',
     'confidence': 'medium', 'notes': 'Mobile subscriptions per 100 people'},
    
    {'record_type': 'event', 'indicator': 'Digital ID Expansion',
     'observation_date': '2024-03-01', 'source_name': 'NBE',
     'confidence': 'medium', 'notes': 'Fayda ID system expansion'}
]

df_enriched = pd.concat([df_unified, pd.DataFrame(new_data)], ignore_index=True)
print(f"✓ Added {len(new_data)} new records")
print(f"✓ Total records now: {len(df_enriched)}")

# Save enriched data
df_enriched.to_csv('../data/processed/ethiopia_fi_enriched.csv', index=False)
print("✓ Enriched data saved to: ../data/processed/ethiopia_fi_enriched.csv")

# Create enrichment log
log_content = f"""# Data Enrichment Log
Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Summary
- Original records: {len(df_unified)}
- Enriched records: {len(df_enriched)}
- New records added: {len(new_data)}

## New Records Added:
1. 2025 Account Ownership Projection (52.5%)
2. 2024 Mobile Penetration Rate (45.2%)
3. Digital ID Expansion Event (March 2024)

## Next Steps:
- Analyze growth patterns
- Identify correlation factors
- Prepare for Task 2 EDA
"""

with open('../reports/data_enrichment_log.md', 'w') as f:
    f.write(log_content)

print("✓ Enrichment log saved to: ../reports/data_enrichment_log.md")

print("\n" + "=" * 60)
print("TASK 1 COMPLETED SUCCESSFULLY!")
print("=" * 60)
