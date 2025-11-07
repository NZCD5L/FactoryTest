#!/usr/bin/env python3
"""
Test script to verify pandas installation and CSV loading
"""
import pandas as pd
import sys

print("=" * 60)
print("Testing FactoryTest Environment Setup")
print("=" * 60)

# Test pandas version
print(f"\n✓ Pandas version: {pd.__version__}")
print(f"✓ Python version: {sys.version.split()[0]}")

# Test loading each CSV
csv_files = ['Companies.csv', 'KPIs_prueba.csv', 'dealflow_prueba.csv']

for csv_file in csv_files:
    try:
        df = pd.read_csv(csv_file)
        print(f"\n✓ {csv_file} loaded successfully")
        print(f"  - Rows: {len(df):,}")
        print(f"  - Columns: {len(df.columns)}")
        print(f"  - Memory: {df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    except Exception as e:
        print(f"\n✗ Error loading {csv_file}: {e}")

print("\n" + "=" * 60)
print("Setup test complete!")
print("=" * 60)
