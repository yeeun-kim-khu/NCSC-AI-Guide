# test_read.py
print("TESTING FILE READING")

import pandas as pd
import os

# Test basic functionality
print("pandas version:", pd.__version__)
print("Current dir:", os.getcwd())

# List files
files = os.listdir('.')
print("\nFiles in directory:")
for f in files:
    if f.endswith(('.xlsx', '.csv')):
        print(f"  {f}")

# Try to read one file
print("\n=== ATTEMPTING TO READ ===")
try:
    # Try CSV first
    csv_files = [f for f in files if f.endswith('.csv')]
    if csv_files:
        print(f"Reading CSV: {csv_files[0]}")
        df = pd.read_csv(csv_files[0], encoding='utf-8')
        print(f"SUCCESS! Shape: {df.shape}")
        print(f"Columns: {list(df.columns)}")
        
        # Show first row
        row = df.iloc[0]
        for col in df.columns:
            val = row[col]
            if pd.notna(val) and str(val) != 'nan':
                print(f"  {col}: {val}")
    else:
        print("No CSV files found")
        
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

print("\n=== TEST COMPLETE ===")
