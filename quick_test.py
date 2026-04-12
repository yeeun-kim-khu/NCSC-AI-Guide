import pandas as pd

# Read one CSV file
csv_file = "C:\\Users\\yeeun\\Documents\\Space Research\\code\\2026\\0406\\C:\\Users\\yeeun\\Documents\\Space Research\\code\\2026\\0406\\"
df = pd.read_csv(csv_file, encoding='utf-8')

print(f"Shape: {df.shape}")
print(f"Columns: {list(df.columns)}")

# Get first row data
first_row = df.iloc[1]
title = str(first_row[df.columns[4]])
content = str(first_row[df.columns[5]])
detail = str(first_row[df.columns[6]])
category = str(first_row[df.columns[1]])

print(f"\nTitle: {title}")
print(f"Content: {content}")
print(f"Detail: {detail}")
print(f"Category: {category}")

# Generate entry
key = f"{category}_{title}"
desc = f"{content}\n{detail}"

print(f"\nGenerated entry:")
print(f'"{key}": """{desc}""",')
