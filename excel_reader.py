# excel_reader.py
import pandas as pd

print("=== EXCEL READER ===")

try:
    # Read Excel file
    df = pd.read_excel("C:\\Users\\yeeun\\Documents\\Space Research\\code\\2026\\0406\\_260407_\\uc218\\uc815.xlsx")
    
    print(f"SUCCESS: Excel file read")
    print(f"Shape: {df.shape}")
    print(f"Columns: {list(df.columns)}")
    
    # Show first row
    print("\nFirst row:")
    row = df.iloc[0]
    for col in df.columns:
        val = row[col]
        if pd.notna(val) and str(val) != 'nan':
            print(f"  {col}: {val}")
    
    # Check exploration zone
    print("\n=== EXPLORATION ZONE ===")
    for i in range(min(5, len(df))):
        row = df.iloc[i]
        title = str(row.get('Title', ''))
        if title and title != 'nan':
            print(f"Row {i+1}: {title}")
    
    # Generate sample RAG entry
    print("\n=== SAMPLE RAG ENTRY ===")
    row = df.iloc[0]
    title = str(row.get('Title', ''))
    content = str(row.get('Content', ''))
    
    if title and title != 'nan':
        print(f'"sample_exhibit": """**{title}**')
        if content and content != 'nan':
            print(f'**Description**: {content}')
        print('"""')
    
except Exception as e:
    print(f"ERROR: {e}")
    
    # Try CSV as fallback
    print("\n=== FALLBACK: CSV ===")
    import os
    csv_files = [f for f in os.listdir('.') if f.endswith('.csv')]
    
    if csv_files:
        csv_file = csv_files[0]
        print(f"Trying CSV: {csv_file}")
        
        try:
            df = pd.read_csv(csv_file, encoding='utf-8')
            print(f"CSV Shape: {df.shape}")
            print(f"CSV Columns: {list(df.columns)}")
            
            # Show first row
            row = df.iloc[0]
            for col in df.columns:
                val = row[col]
                if pd.notna(val) and str(val) != 'nan':
                    print(f"  {col}: {val}")
                    
        except Exception as e2:
            print(f"CSV Error: {e2}")
    else:
        print("No CSV files found")
