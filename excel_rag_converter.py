# excel_rag_converter.py
import pandas as pd
import json

def convert_excel_to_rag(excel_file_path):
    """
    Convert Excel exhibit data to RAG format with image handling
    """
    
    try:
        # Read Excel file
        df = pd.read_excel(excel_file_path)
        
        print("Excel columns:", df.columns.tolist())
        print(f"Total rows: {len(df)}")
        
        # Convert to RAG format
        rag_entries = {}
        
        for idx, row in df.iterrows():
            # Extract key information
            exhibit_id = str(row.get('ID', f'exhibit_{idx}'))
            category = str(row.get('Category', row.get('Category', row.get('Category', ''))))
            title = str(row.get('Title', row.get('Title', row.get('Title', ''))))
            content = str(row.get('Content', row.get('Content', row.get('Content', ''))))
            detail = str(row.get('Detail', row.get('Detail', row.get('Detail', ''))))
            caution = str(row.get('Caution', row.get('Caution', row.get('Caution', ''))))
            status = str(row.get('Status', row.get('Status', row.get('Status', ''))))
            
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
            
            if caution and caution != 'nan':
                description_parts.append(f"**Important Notes**: {caution}")
            
            if status and status != 'nan':
                description_parts.append(f"**Status**: {status}")
            
            # Create unique key
            key = f"{category}_{title}" if category and title else exhibit_id
            key = key.replace(" ", "_").replace("/", "_").replace("(", "").replace(")", "")
            
            # Join all parts
            full_description = "\n".join(description_parts)
            
            if full_description:
                rag_entries[key] = full_description
        
        # Generate Python code for constants.py
        python_code = "# === Excel Data Additions ===\n"
        python_code += "# Generated from Excel file\n\n"
        
        for key, description in rag_entries.items():
            python_code += f'    "{key}": """{description}""",\n\n'
        
        # Save to file
        with open("excel_rag_output.py", "w", encoding="utf-8") as f:
            f.write(python_code)
        
        print(f"Successfully converted {len(rag_entries)} entries!")
        print("Output saved to: excel_rag_output.py")
        print("\nCopy the content from excel_rag_output.py and paste it into constants.py")
        
        return rag_entries
        
    except Exception as e:
        print(f"Error: {e}")
        return None

def manual_format_example():
    """
    Show manual format for Excel data
    """
    example = '''
# === Excel Data Additions ===
# Format based on your Excel structure:

"category_exhibit_title": """**Exhibit Title**
**Description**: Main content from Excel
**Details**: Detailed explanation
**Category**: Exhibit category
**Important Notes**: Safety/caution information
**Status**: Current status
**Note**: Images are referenced but not included in RAG text""",

'''
    print("Manual format example:")
    print(example)

if __name__ == "__main__":
    # Usage
    print("Excel to RAG Converter")
    print("=" * 30)
    print("1. Use automatic converter: python excel_rag_converter.py your_file.xlsx")
    print("2. Or use manual format below")
    print()
    manual_format_example()
