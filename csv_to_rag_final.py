# csv_to_rag_final.py - Final CSV processing
import pandas as pd
import os

def process_csv_files():
    """Process all CSV files and generate RAG entries"""
    
    # Korean CSV files
    csv_files = [
        "C:\\Users\\yeeun\\Documents\\Space Research\\code\\2026\\0406\\국립어린이과학관 전시물품 대장_260407 - AI놀이터.csv",
        "C:\\Users\\yeeun\\Documents\\Space Research\\code\\2026\\0406\\국립어린이과학관 전시물품 대장_260407 - 관찰놀이터.csv",
        "C:\\Users\\yeeun\\Documents\\Space Research\\code\\2026\\0406\\국립어린이과학관 전시물품 대장_260407 - 탐구놀이터.csv",
        "C:\\Users\\yeeun\\Documents\\Space Research\\code\\2026\\0406\\국립어린이과학관 전시물품 대장_260407 - 행동놀이터.csv"
    ]
    
    all_entries = {}
    
    for csv_file in csv_files:
        try:
            print(f"Processing: {os.path.basename(csv_file)}")
            df = pd.read_csv(csv_file, encoding='utf-8')
            
            print(f"  Columns: {list(df.columns)}")
            print(f"  Rows: {len(df)}")
            
            # Show sample data
            if len(df) > 0:
                sample = df.iloc[0]
                print("  Sample row:")
                for col in df.columns[:5]:
                    val = sample[col]
                    if pd.notna(val) and str(val) != 'nan':
                        print(f"    {col}: {str(val)[:50]}...")
            
            # Process entries
            for idx, row in df.iterrows():
                # Get data from columns (adjust column names as needed)
                title = str(row.get(df.columns[4], ''))  # Unnamed: 4 (Title)
                content = str(row.get(df.columns[5], ''))  # Unnamed: 5 (Content)
                detail = str(row.get(df.columns[6], ''))   # Unnamed: 6 (Detail)
                category = str(row.get(df.columns[1], '')) # Unnamed: 1 (Category)
                
                # Skip empty titles
                if not title or title == 'nan':
                    continue
                
                # Create description
                desc_parts = [f"**{title}**"]
                if content and content != 'nan':
                    desc_parts.append(f"**Description**: {content}")
                if detail and detail != 'nan':
                    desc_parts.append(f"**Details**: {detail}")
                if category and category != 'nan':
                    desc_parts.append(f"**Category**: {category}")
                
                # Create unique key
                key = title.replace(" ", "_").replace("/", "_").replace("(", "").replace(")", "")
                
                # Add to entries
                all_entries[key] = "\n".join(desc_parts)
            
            print(f"  Processed {len(df)} entries from {csv_file}")
            
        except FileNotFoundError:
            print(f"  File not found: {csv_file}")
        except Exception as e:
            print(f"  Error processing {csv_file}: {e}")
    
    return all_entries

def generate_constants_code():
    """Generate code for constants.py"""
    
    entries = process_csv_files()
    
    if not entries:
        print("No entries found!")
        return
    
    print(f"Total entries: {len(entries)}")
    
    # Show sample
    print("\nSample entries:")
    for i, (key, desc) in enumerate(list(entries.items())[:3]):
        print(f"{i+1}. {key}")
        print(f"   {desc[:80]}...")
    
    # Generate code
    print("\n" + "="*60)
    print("ADD THIS TO constants.py:")
    print("="*60)
    
    print("\n    # === Excel Data Additions ===")
    print(f"    # Total {len(entries)} entries from Excel files\n")
    
    for key, desc in entries.items():
        # Escape triple quotes
        escaped_desc = desc.replace('"""', '\\"\\"\\"')
        print(f'    "{key}": """{escaped_desc}""",\n')
    
    print("}")
    print("="*60)
    print("Copy the code above and paste it into constants.py")
    print("Before the closing brace of STATIC_EXHIBIT_INFO")
    print("\nAfter adding, restart with: streamlit run app.py")

if __name__ == "__main__":
    generate_constants_code()
