# csv_to_rag_fixed.py
import pandas as pd
import os

def convert_csv_to_rag():
    """
    Convert all CSV files in the directory to RAG format
    """
    
    # Correct file paths
    csv_files = [
        "C:\\Users\\yeeun\\Documents\\Space Research\\code\\2026\\0406\\_260407 - AI Playground.csv",
        "C:\\Users\\yeeun\\Documents\\Space Research\\code\\2026\\0406\\_260407 - Observation Playground.csv",
        "C:\\Users\\yeeun\\Documents\\Space Research\\code\\2026\\0406\\_260407 - Exploration Playground.csv",
        "C:\\Users\\yeeun\\Documents\\Space Research\\code\\2026\\0406\\_260407 - Action Playground.csv"
    ]
    
    all_entries = {}
    
    for csv_file in csv_files:
        if os.path.exists(csv_file):
            try:
                # Read CSV file
                df = pd.read_csv(csv_file, encoding='utf-8')
                
                print(f"Processing: {os.path.basename(csv_file)}")
                print(f"Columns: {df.columns.tolist()}")
                print(f"Rows: {len(df)}")
                
                # Process each row
                for idx, row in df.iterrows():
                    # Extract information
                    exhibit_id = str(row.get('ID', f'exhibit_{idx}'))
                    category = str(row.get('Category', row.get('Category', row.get('Category', '')))
                    exhibit_type = str(row.get('Exhibit Type', row.get('Exhibit Type', row.get('Exhibit Type', '')))
                    operation = str(row.get('Operation', row.get('Operation', row.get('Operation', '')))
                    title = str(row.get('Title', row.get('Title', row.get('Title', '')))
                    content = str(row.get('Content', row.get('Content', row.get('Content', '')))
                    detail = str(row.get('Detail', row.get('Detail', row.get('Detail', '')))
                    caution = str(row.get('Caution', row.get('Caution', row.get('Caution', '')))
                    status = str(row.get('Status', row.get('Status', row.get('Status', '')))
                    
                    # Create comprehensive description
                    description_parts = []
                    
                    if title and title != 'nan':
                        description_parts.append(f"**{title}**")
                    
                    if content and content != 'nan':
                        description_parts.append(f"**Description**: {content}")
                    
                    if detail and detail != 'nan':
                        description_parts.append(f"**Details**: {detail}")
                    
                    if category and category != 'nan':
                        description_parts.append(f"**Category**: {category}")
                    
                    if exhibit_type and exhibit_type != 'nan':
                        description_parts.append(f"**Exhibit Type**: {exhibit_type}")
                    
                    if operation and operation != 'nan':
                        description_parts.append(f"**Operation**: {operation}")
                    
                    if caution and caution != 'nan':
                        description_parts.append(f"**Important Notes**: {caution}")
                    
                    if status and status != 'nan':
                        description_parts.append(f"**Status**: {status}")
                    
                    # Create unique key
                    key_base = title if title and title != 'nan' else exhibit_id
                    key = f"{category}_{key_base}" if category and category != 'nan' else key_base
                    key = key.replace(" ", "_").replace("/", "_").replace("(", "").replace(")", "").replace("-", "_")
                    
                    # Join all parts
                    full_description = "\n".join(description_parts)
                    
                    if full_description and len(full_description) > 10:  # Skip empty entries
                        all_entries[key] = full_description
                
                print(f"  Processed {len(df)} rows\n")
                
            except Exception as e:
                print(f"Error processing {csv_file}: {e}")
        else:
            print(f"File not found: {csv_file}")
    
    return all_entries

def update_constants_with_excel_data():
    """
    Update constants.py with Excel data
    """
    
    # Convert CSV to RAG format
    rag_entries = convert_csv_to_rag()
    
    if not rag_entries:
        print("No entries found!")
        return
    
    print(f"Total entries to add: {len(rag_entries)}")
    
    # Read current constants.py
    with open("constants.py", "r", encoding="utf-8") as f:
        content = f.read()
    
    # Find the position to insert new data (before the closing brace)
    insert_pos = content.rfind("}")
    
    if insert_pos == -1:
        print("Could not find closing brace in constants.py")
        return
    
    # Generate Python code for new entries
    new_entries_code = "\n    # === Excel Data Additions ===\n"
    new_entries_code += f"    # Total {len(rag_entries)} entries from Excel files\n\n"
    
    for key, description in rag_entries.items():
        # Clean up the description for Python string
        clean_desc = description.replace('"""', '\\"\\"\\"').replace('\n', '\\n')
        new_entries_code += f'    "{key}": """{description}""",\n\n'
    
    # Insert new entries
    updated_content = content[:insert_pos] + new_entries_code + content[insert_pos:]
    
    # Write updated constants.py
    with open("constants_updated.py", "w", encoding="utf-8") as f:
        f.write(updated_content)
    
    print("Updated constants.py saved as: constants_updated.py")
    print("Review the file and replace constants.py if satisfied.")
    
    # Show sample entries
    print("\nSample entries:")
    for i, (key, desc) in enumerate(list(rag_entries.items())[:3]):
        print(f"\n{i+1}. {key}")
        print(f"   {desc[:100]}...")

if __name__ == "__main__":
    update_constants_with_excel_data()
