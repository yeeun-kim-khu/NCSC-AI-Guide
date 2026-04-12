# rag.py
import os
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from config import STATIC_EXHIBIT_INFO, CSC_URLS
import pandas as pd
from multilingual_loader import load_multilingual_brochures

def load_csv_data():
    """CSV files from current directory - real-time loading"""
    csv_files = [
        "C:\\Users\\yeeun\\Documents\\Space Research\\code\\2026\\0406\\국립어린이과학관 전시물품 대장_260407 - AI놀이터.csv",
        "C:\\Users\\yeeun\\Documents\\Space Research\\code\\2026\\0406\\국립어린이과학관 전시물품 대장_260407 - 관찰놀이터.csv",
        "C:\\Users\\yeeun\\Documents\\Space Research\\code\\2026\\0406\\국립어린이과학관 전시물품 대장_260407 - 탐구놀이터.csv",
        "C:\\Users\\yeeun\\Documents\\Space Research\\code\\2026\\0406\\국립어린이과학관 전시물품 대장_260407 - 행동놀이터.csv"
    ]
    
    docs = []
    
    for csv_file in csv_files:
        if os.path.exists(csv_file):
            try:
                # skiprows=1로 첫 번째 행(전시관 제목) 건너뛰고, 2행을 헤더로 사용
                df = pd.read_csv(csv_file, encoding='utf-8', skiprows=1)
                
                print(f"Loading {os.path.basename(csv_file)}: {len(df)} rows")
                
                for idx, row in df.iterrows():
                    # 컬럼명으로 접근
                    category = str(row.get('분류', '')).strip()
                    title = str(row.get('제목', '')).strip()
                    content = str(row.get('내용', '')).strip()
                    detail = str(row.get('세부 설명', '')).strip()
                    
                    # 유효한 데이터만 추가
                    if title and title != 'nan' and len(title) > 0:
                        # 놀이터 이름 추출 (파일명에서)
                        zone_name = ""
                        if "AI놀이터" in csv_file:
                            zone_name = "AI놀이터"
                        elif "탐구놀이터" in csv_file:
                            zone_name = "탐구놀이터"
                        elif "관찰놀이터" in csv_file:
                            zone_name = "관찰놀이터"
                        elif "행동놀이터" in csv_file:
                            zone_name = "행동놀이터"
                        
                        # Create RAG document
                        text = f"[{zone_name}] {title}\n분류: {category}\n내용: {content}\n세부설명: {detail}"
                        metadata = {
                            "source": f"csv_{zone_name}", 
                            "title": title, 
                            "category": zone_name,  # 놀이터 이름을 category로 저장
                            "subcategory": category  # 원래 분류는 subcategory로
                        }
                        docs.append(Document(page_content=text, metadata=metadata))
                        
            except Exception as e:
                print(f"CSV load error {csv_file}: {e}")
                import traceback
                traceback.print_exc()
    
    return docs

def initialize_vector_db():
    """정적 전시관 정보를 Chroma Vector DB로 구성합니다."""
    persist_directory = "./chroma_db"
    collection_name = "csc_exhibits"
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    
    try:
        # 먼저 기존 컬렉션을 로드 시도
        vectorstore = Chroma(
            persist_directory=persist_directory,
            collection_name=collection_name,
            embedding_function=embeddings
        )
        return vectorstore
    except Exception:
        # CSV + static data - real-time loading
        docs = []
        
        # Add static data
        for name, desc in STATIC_EXHIBIT_INFO.items():
            url = CSC_URLS.get(name, "https://www.csc.go.kr")
            docs.append(Document(page_content=f"[{name}] {desc}", metadata={"source": url}))
        
        # Add CSV data
        csv_docs = load_csv_data()
        docs.extend(csv_docs)
        
        # Add multilingual data
        multilingual_docs = load_multilingual_brochures()
        docs.extend(multilingual_docs)
        
        print(f"Loaded {len(csv_docs)} CSV entries + {len(multilingual_docs)} multilingual entries + {len(STATIC_EXHIBIT_INFO)} static entries")
        
        vectorstore = Chroma.from_documents(
            docs, 
            embeddings,
            persist_directory=persist_directory,
            collection_name=collection_name
        )
        return vectorstore