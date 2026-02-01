import pandas as pd
import numpy as np
from datetime import datetime

# Load original data (adjust path as needed)
original = pd.read_csv('data/raw/ethiopia_fi_unified_data.csv')

# Create enriched version with additional records
# This is a simplified example - adjust based on your actual enrichments

# Add sample infrastructure records
infra_data = {
    'record_type': ['observation'] * 5,
    'pillar': ['infrastructure'] * 5,
    'indicator': ['4G Coverage (%)', 'Smartphone Penetration (%)', 
                  'Agent Density', 'ATM per 100k adults', 'Bank Branches per 100k adults'],
    'indicator_code': ['INF_4G_COVERAGE', 'INF_SMARTPHONE', 'INF_AGENT_DENSITY',
                       'INF_ATM_DENSITY', 'INF_BANK_DENSITY'],
    'value_numeric': [45, 35, 120, 8, 5],
    'observation_date': ['2024-12-01'] * 5,
    'source_name': ['GSMA', 'Ethio Telecom', 'NBE', 'IMF FAS', 'IMF FAS'],
    'confidence': ['high', 'medium', 'high', 'high', 'high']
}

infra_df = pd.DataFrame(infra_data)

# Combine with original
enriched = pd.concat([original, infra_df], ignore_index=True)

# Save enriched dataset
enriched.to_csv('data/processed/ethiopia_fi_enriched.csv', index=False)
print(f"Enriched dataset saved with {len(enriched)} records")
