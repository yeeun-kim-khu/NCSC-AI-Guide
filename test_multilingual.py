import os
from multilingual_loader import create_sample_multilingual_files, load_multilingual_brochures

# Create folder and files
create_sample_multilingual_files()

# Check files
multilingual_dir = "multilingual"
if os.path.exists(multilingual_dir):
    files = os.listdir(multilingual_dir)
    print(f"Files in multilingual folder: {files}")
    
    # Test loading
    docs = load_multilingual_brochures()
    print(f"Loaded {len(docs)} multilingual documents")
    
    for doc in docs:
        print(f"\nLanguage: {doc.metadata['language']}")
        print(f"Source: {doc.metadata['source']}")
        print(f"Content preview: {doc.page_content[:100]}...")
else:
    print("Multilingual folder not found")
