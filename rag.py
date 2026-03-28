# rag.py
import os
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from constants import STATIC_EXHIBIT_INFO, CSC_URLS

def initialize_vector_db():
    """정적 전시관 정보를 Chroma Vector DB로 구성합니다."""
    persist_directory = "./chroma_db"
    collection_name = "csc_exhibits"
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    
    # 이미 저장된 벡터 DB가 있으면 로드 (API 호출 없음)
    if os.path.exists(persist_directory):
        vectorstore = Chroma(
            persist_directory=persist_directory,
            collection_name=collection_name,
            embedding_function=embeddings
        )
        return vectorstore
    
    # 없으면 새로 생성 (최초 1회만 API 호출)
    docs = []
    for name, desc in STATIC_EXHIBIT_INFO.items():
        url = CSC_URLS.get(name, CSC_URLS["홈페이지"])
        docs.append(Document(page_content=f"[{name}] {desc}", metadata={"source": url}))
    
    vectorstore = Chroma.from_documents(
        docs, 
        embeddings,
        persist_directory=persist_directory,
        collection_name=collection_name
    )
    return vectorstore