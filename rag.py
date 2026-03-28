# rag.py
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from constants import STATIC_EXHIBIT_INFO, CSC_URLS

def initialize_vector_db():
    """정적 전시관 정보를 Chroma Vector DB로 구성합니다."""
    docs = []
    for name, desc in STATIC_EXHIBIT_INFO.items():
        url = CSC_URLS.get(name, CSC_URLS["홈페이지"])
        # 문서 내용과 출처를 메타데이터로 저장
        docs.append(Document(page_content=f"[{name}] {desc}", metadata={"source": url}))
    
    # OpenAI의 텍스트 임베딩 모델 사용
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    vectorstore = Chroma.from_documents(docs, embeddings)
    return vectorstore