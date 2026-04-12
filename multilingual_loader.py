# multilingual_loader.py
import os
import pandas as pd
from langchain_core.documents import Document

def load_multilingual_brochures():
    """Load multilingual brochure data for RAG system"""
    
    # Create multilingual folder structure
    multilingual_dir = os.path.join(os.path.dirname(__file__), "multilingual")
    
    # File patterns for different languages (actual brochure naming format)
    brochure_files = {
        "english": {
            "files": [
                os.path.join(multilingual_dir, "Science Center Information_ENG_250318.pdf"),
                os.path.join(multilingual_dir, "Science Center Information_ENG_250318.txt"),
                os.path.join(multilingual_dir, "Science Center Information_ENG_250318.csv")
            ],
            "language": "English"
        },
        "japanese": {
            "files": [
                os.path.join(multilingual_dir, "Science Center Information_JPN_250318.pdf"),
                os.path.join(multilingual_dir, "Science Center Information_JPN_250318.txt"),
                os.path.join(multilingual_dir, "Science Center Information_JPN_250318.csv")
            ],
            "language": "Japanese"
        },
        "chinese": {
            "files": [
                os.path.join(multilingual_dir, "Science Center Information_CHN_250318.pdf"),
                os.path.join(multilingual_dir, "Science Center Information_CHN_250318.txt"),
                os.path.join(multilingual_dir, "Science Center Information_CHN_250318.csv")
            ],
            "language": "Chinese"
        }
    }
    
    docs = []
    
    for lang_code, lang_info in brochure_files.items():
        for file_path in lang_info["files"]:
            if os.path.exists(file_path):
                try:
                    # Handle different file types
                    if file_path.endswith('.csv'):
                        df = pd.read_csv(file_path, encoding='utf-8')
                        for idx, row in df.iterrows():
                            if pd.notna(row.iloc[0]):  # Check if first column has content
                                content = ' '.join([str(val) for val in row if pd.notna(val)])
                                text = f"[{lang_info['language']}] {content}"
                                metadata = {
                                    "source": f"multilingual_{lang_code}",
                                    "language": lang_info["language"],
                                    "file_type": "csv"
                                }
                                docs.append(Document(page_content=text, metadata=metadata))
                    
                    elif file_path.endswith('.txt'):
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            text = f"[{lang_info['language']}] {content}"
                            metadata = {
                                "source": f"multilingual_{lang_code}",
                                "language": lang_info["language"],
                                "file_type": "txt"
                            }
                            docs.append(Document(page_content=text, metadata=metadata))
                    
                    elif file_path.endswith('.pdf'):
                        # For PDF files, you might need to install PyPDF2 or similar
                        # This is a placeholder for PDF processing
                        text = f"[{lang_info['language']}] Brochure content available in PDF format"
                        metadata = {
                            "source": f"multilingual_{lang_code}",
                            "language": lang_info["language"],
                            "file_type": "pdf"
                        }
                        docs.append(Document(page_content=text, metadata=metadata))
                        
                except Exception as e:
                    print(f"Error loading {file_path}: {e}")
    
    return docs

def create_sample_multilingual_files():
    """Create sample multilingual files for testing"""
    
    multilingual_dir = os.path.join(os.path.dirname(__file__), "multilingual")
    os.makedirs(multilingual_dir, exist_ok=True)
    
    # Sample English brochure
    english_content = """National Children's Science Center Visitor Guide
    
Welcome to the National Children's Science Center!
    
Exhibition Zones:
- AI Zone: Experience artificial intelligence and robotics
- Observation Zone: Discover through careful observation
- Exploration Zone: Experiment with scientific principles
- Action Zone: Learn through physical activities
- Thinking Zone: Develop problem-solving skills
    
Operating Hours: 09:30-17:30 (Last admission 17:00)
Closed: Every Monday (except holidays)
    
Admission:
- Adults (20-64): 2,000 KRW
- Youth/Children (7-19): 1,000 KRW
- Free: Under 6, over 65, disabled
    
Address: 215 Changgyeonggung-ro, Jongno-gu, Seoul
"""
    
    # Sample Japanese brochure
    japanese_content = """ nationalsciencecenter
    
National Children's Science Center Visitor Guide
    
AI Zone: Artificial intelligence experience
Observation Zone: Scientific discovery
Exploration Zone: Hands-on experiments
Action Zone: Physical learning
Thinking Zone: Problem solving
    
Hours: 09:30-17:30
Closed: Mondays
    
Admission: Adults 2,000 KRW, Children 1,000 KRW
Address: Seoul, Jongno-gu, Changgyeonggung-ro 215
"""
    
    # Sample Chinese brochure
    chinese_content = """National Children's Science Center Visitor Guide
    
Welcome to Korea's National Science Center!
    
AI Zone: Artificial intelligence and robotics
Observation Zone: Scientific observation
Exploration Zone: Experimental learning
Action Zone: Physical activities
Thinking Zone: Creative thinking
    
Hours: 09:30-17:30
Closed: Mondays
    
Admission: Adults 2,000 KRW, Children 1,000 KRW
Address: Seoul, Jongno District, Changgyeonggung Road 215
"""
    
    # Write sample files with actual naming format
    with open(os.path.join(multilingual_dir, "Science Center Information_ENG_250318.txt"), 'w', encoding='utf-8') as f:
        f.write(english_content)
    
    with open(os.path.join(multilingual_dir, "Science Center Information_JPN_250318.txt"), 'w', encoding='utf-8') as f:
        f.write(japanese_content)
    
    with open(os.path.join(multilingual_dir, "Science Center Information_CHN_250318.txt"), 'w', encoding='utf-8') as f:
        f.write(chinese_content)
    
    print(f"Created sample multilingual files in {multilingual_dir}")

if __name__ == "__main__":
    create_sample_multilingual_files()
    docs = load_multilingual_brochures()
    print(f"Loaded {len(docs)} multilingual documents")
    for doc in docs[:3]:  # Show first 3 documents
        print(f"\nLanguage: {doc.metadata['language']}")
        print(f"Content: {doc.page_content[:100]}...")
