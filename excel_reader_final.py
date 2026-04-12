# excel_reader_final.py
import pandas as pd
import os

print("=== FINAL EXCEL READER ===")

# Find Excel files
excel_files = [f for f in os.listdir('.') if f.endswith('.xlsx')]
print(f"Excel files: {excel_files}")

if excel_files:
    excel_file = excel_files[0]
    print(f"\nReading: {excel_file}")
    
    try:
        df = pd.read_excel(excel_file)
        print(f"SUCCESS! Shape: {df.shape}")
        print(f"Columns: {list(df.columns)}")
        
        # Show first 3 rows
        print("\nFirst 3 rows:")
        for i in range(min(3, len(df))):
            print(f"Row {i+1}:")
            row = df.iloc[i]
            for col in df.columns:
                val = row[col]
                if pd.notna(val) and str(val) != 'nan':
                    print(f"  {col}: {val}")
            print()
        
        # Generate RAG entries
        print("=== RAG ENTRIES ===")
        entries = {}
        
        for idx, row in df.iterrows():
            title = str(row.get('Title', ''))
            content = str(row.get('Content', ''))
            
            if title and title != 'nan':
                desc_parts = [f"**{title}**"]
                if content and content != 'nan':
                    desc_parts.append(f"**Description**: {content}")
                
                key = title.replace(" ", "_").replace("/", "_").replace("(", "").replace(")", "")
                entries[key] = "\n".join(desc_parts)
        
        print(f"Generated {len(entries)} entries")
        
        # Show sample
        print("\nSample entries:")
        for i, (key, desc) in enumerate(list(entries.items())[:3]):
            print(f"{i+1}. {key}")
            print(f"   {desc[:80]}...")
        
        # Generate code for constants.py
        print("\n=== CODE FOR constants.py ===")
        print("Replace the sample entries with this:\n")
        
        for key, desc in list(entries.items())[:5]:
            escaped_desc = desc.replace('"""', '\\"\\"\\"')
            print(f'    "{key}": """{escaped_desc}""",\n')
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        
        # Try CSV files
        print("\n=== TRYING CSV FILES ===")
        csv_files = [f for f in os.listdir('.') if f.endswith('.csv')]
        print(f"CSV files: {csv_files}")
        
        if csv_files:
            csv_file = csv_files[0]
            print(f"\nReading CSV: {csv_file}")
            
            try:
                df = pd.read_csv(csv_file, encoding='utf-8')
                print(f"CSV SUCCESS! Shape: {df.shape}")
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
    print("No Excel files found!")
