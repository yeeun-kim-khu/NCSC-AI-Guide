import pandas as pd
import os

# Test CSV loading with correct paths
csv_files = [
    "C:\\Users\\yeeun\\Documents\\Space Research\\code\\2026\\0406\\",
    "C:\\Users\\yeeun\\Documents\\Space Research\\code\\2026\\0406\\",
    "C:\\Users\\yeeun\\Documents\\Space Research\\code\\2026\\0406\\",
    "C:\\Users\\yeeun\\Documents\\Space Research\\code\\2026\\0406\\"
]

print("Testing CSV file loading...")

for csv_file in csv_files:
    if os.path.exists(csv_file):
        print(f"Found: {os.path.basename(csv_file)}")
        try:
            df = pd.read_csv(csv_file, encoding='utf-8')
            print(f"  Shape: {df.shape}")
            print(f"  Columns: {list(df.columns)}")
            
            # Show first data row
            if len(df) > 1:
                row = df.iloc[1]
                category = str(row.iloc[1]).strip()
                title = str(row.iloc[4]).strip()
                print(f"  Sample: {category} - {title}")
        except Exception as e:
            print(f"  Error: {e}")
    else:
        print(f"Not found: {csv_file}")
