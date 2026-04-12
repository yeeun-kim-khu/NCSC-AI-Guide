# excel_to_rag.py
import pandas as pd
import json

def convert_excel_to_constants(excel_file_path, output_file="constants.py"):
    """
    Convert Excel file to RAG-compatible constants format
    
    Args:
        excel_file_path: Path to your Excel file
        output_file: Output constants file path
    """
    
    try:
        # Read Excel file
        df = pd.read_excel(excel_file_path)
        
        print("Excel file columns:", df.columns.tolist())
        print("First few rows:")
        print(df.head())
        
        # Convert to dictionary format for RAG
        exhibit_info = {}
        
        # Assuming Excel has columns like 'category', 'title', 'description'
        for _, row in df.iterrows():
            # Adjust column names based on your Excel structure
            category = str(row.get('category', row.get('Category', row.get('Category', ''))))
            title = str(row.get('title', row.get('Title', row.get('Title', ''))))
            description = str(row.get('description', row.get('Description', row.get('Description', ''))))
            
            if title and description:
                key = f"{category}_{title}" if category else title
                exhibit_info[key] = description
        
        # Read existing constants.py
        with open("constants.py", "r", encoding="utf-8") as f:
            content = f.read()
        
        # Find STATIC_EXHIBIT_INFO section and append new data
        insert_point = content.find("STATIC_EXHIBIT_INFO = {")
        if insert_point == -1:
            print("Error: STATIC_EXHIBIT_INFO not found in constants.py")
            return
        
        # Find the closing brace of STATIC_EXHIBIT_INFO
        brace_count = 0
        end_point = insert_point
        for i, char in enumerate(content[insert_point:], insert_point):
            if char == "{":
                brace_count += 1
            elif char == "}":
                brace_count -= 1
                if brace_count == 0:
                    end_point = i + 1
                    break
        
        # Create new entries
        new_entries = "\n    # Excel data additions\n"
        for key, value in exhibit_info.items():
            # Clean key for Python dictionary
            clean_key = key.replace(" ", "_").replace("-", "_").replace("(", "").replace(")", "")
            new_entries += f'    "{clean_key}": """{value}""",\n'
        
        # Insert new data before the closing brace
        updated_content = content[:end_point-1] + new_entries + content[end_point-1:]
        
        # Write updated constants.py
        with open("constants_updated.py", "w", encoding="utf-8") as f:
            f.write(updated_content)
        
        print(f"Successfully processed {len(exhibit_info)} entries!")
        print("Updated file saved as: constants_updated.py")
        print("Review the file and replace constants.py if satisfied.")
        
        return exhibit_info
        
    except Exception as e:
        print(f"Error processing Excel file: {e}")
        return None

def manual_add_example():
    """
    Example of how to manually add Excel data to constants.py
    """
    example_excel_data = """
    # Example: Add this to STATIC_EXHIBIT_INFO in constants.py
    
    "new_exhibit_1": """This is a new exhibit from your Excel file. 
    Description includes details about what visitors can see and learn.
    Target audience: Elementary school students
    Features: Interactive displays, hands-on activities""",
    
    "new_exhibit_2": """Another exhibit from Excel data.
    This description explains the scientific principles and activities.
    Location: 2nd floor, Room 203
    Duration: Recommended 30 minutes""",
    """
    
    print("Manual addition example:")
    print(example_excel_data)

if __name__ == "__main__":
    # Usage:
    # python excel_to_rag.py "your_excel_file.xlsx"
    
    import sys
    
    if len(sys.argv) > 1:
        excel_file = sys.argv[1]
        convert_excel_to_constants(excel_file)
    else:
        print("Usage: python excel_to_rag.py <excel_file_path>")
        print("\nOr use manual addition method:")
        manual_add_example()
