import pandas as pd
import os

# Test one CSV file
csv_file = "C:\\Users\\yeeun\\Documents\\Space Research\\code\\2026\\0406\\_260407 - AI Playground.csv"

try:
    print(f"Testing: {os.path.basename(csv_file)}")
    df = pd.read_csv(csv_file, encoding='utf-8')
    
    print(f"Columns: {list(df.columns)}")
    print(f"Rows: {len(df)}")
    
    # Check first few rows
    print("\nFirst 3 rows:")
    for i in range(min(3, len(df))):
        print(f"Row {i+1}:")
        for col in df.columns[:7]:
            val = df.iloc[i][col]
            if pd.notna(val) and str(val) != 'nan':
                print(f"  {col}: {str(val)[:30]}...")
        print()
        
except Exception as e:
    print(f"Error: {e}")
