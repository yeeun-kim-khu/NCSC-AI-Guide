#!/usr/bin/env python3
import pandas as pd
import os

def test_csv_output():
    """Test CSV processing and show output"""
    
    csv_files = [
        "C:\\Users\\yeeun\\Documents\\Space Research\\code\\2026\\0406\\\\C:\\Users\\yeeun\\Documents\\Space Research\\code\\2026\\0406\\\\C:\\Users\\yeeun\\Documents\\Space Research\\code\\2026\\0406\\\\C:\\Users\\yeeun\\Documents\\Space Research\\code\\2026\\0406\\\\C:\\Users\\yeeun\\Documents\\Space Research\\code\\2026\\0406\\"
    ]
    
    entries = {}
    
    for csv_file in csv_files:
        if os.path.exists(csv_file):
            print(f"Processing: {csv_file}")
            
            try:
                df = pd.read_csv(csv_file, encoding='utf-8')
                print(f"Shape: {df.shape}")
                print(f"Columns: {list(df.columns)}")
                
                # Process first row
                for idx, row in df.iterrows():
                    if idx >= 1:  # Only first row for test
                        break
                        
                    title = str(row.get(df.columns[4], ''))
                    content = str(row.get(df.columns[5], ''))
                    detail = str(row.get(df.columns[6], ''))
                    category = str(row.get(df.columns[1], ''))
                    
                    if title and title != 'nan':
                        key = f"{category}_{title}"
                        desc = f"{content}\n{detail}"
                        entries[key] = desc
                        print(f"Generated: {key}")
                        break
                        
            except Exception as e:
                print(f"Error: {e}")
        else:
            print(f"File not found: {csv_file}")
    
    # Generate constants code
    print("\n" + "="*60)
    print("GENERATED CODE:")
    print("="*60)
    
    for key, desc in entries.items():
        escaped_desc = desc.replace('"""', '\\"\\"\\"')
        print(f'    "{key}": """{escaped_desc}""",\n')

if __name__ == "__main__":
    test_csv_output()
