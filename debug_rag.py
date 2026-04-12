# debug_rag.py - RAG 데이터 확인 스크립트
import pandas as pd
import os
from rag import initialize_vector_db, load_csv_data

def check_csv_files():
    """CSV 파일 내용 확인"""
    csv_files = [
        "C:\\Users\\yeeun\\Documents\\Space Research\\code\\2026\\0406\\국립어린이과학관 전시물품 대장_260407 - AI놀이터.csv",
        "C:\\Users\\yeeun\\Documents\\Space Research\\code\\2026\\0406\\국립어린이과학관 전시물품 대장_260407 - 관찰놀이터.csv",
        "C:\\Users\\yeeun\\Documents\\Space Research\\code\\2026\\0406\\국립어린이과학관 전시물품 대장_260407 - 탐구놀이터.csv",
        "C:\\Users\\yeeun\\Documents\\Space Research\\code\\2026\\0406\\국립어린이과학관 전시물품 대장_260407 - 행동놀이터.csv"
    ]
    
    print("=" * 80)
    print("CSV 파일 확인")
    print("=" * 80)
    
    for csv_file in csv_files:
        if os.path.exists(csv_file):
            print(f"\n📁 파일: {os.path.basename(csv_file)}")
            try:
                df = pd.read_csv(csv_file, encoding='utf-8')
                print(f"   총 행 수: {len(df)}")
                print(f"   컬럼: {df.columns.tolist()}")
                
                # 첫 3행 확인
                print("\n   첫 3행 데이터:")
                for idx, row in df.head(3).iterrows():
                    category = str(row.iloc[1]).strip() if len(row) > 1 else "N/A"
                    title = str(row.iloc[4]).strip() if len(row) > 4 else "N/A"
                    print(f"   [{idx}] Category: {category}, Title: {title}")
                    
            except Exception as e:
                print(f"   ❌ 오류: {e}")
        else:
            print(f"\n❌ 파일 없음: {csv_file}")

def check_loaded_docs():
    """load_csv_data() 함수로 로드된 문서 확인"""
    print("\n" + "=" * 80)
    print("load_csv_data() 결과 확인")
    print("=" * 80)
    
    docs = load_csv_data()
    print(f"\n총 로드된 문서 수: {len(docs)}")
    
    # 놀이터별 문서 개수
    category_counts = {}
    for doc in docs:
        category = doc.metadata.get('category', 'Unknown')
        category_counts[category] = category_counts.get(category, 0) + 1
    
    print("\n놀이터별 문서 개수:")
    for category, count in sorted(category_counts.items()):
        print(f"   {category}: {count}개")
    
    # 샘플 문서 3개 출력
    print("\n샘플 문서 (처음 3개):")
    for i, doc in enumerate(docs[:3]):
        print(f"\n   [{i+1}] Category: {doc.metadata.get('category')}")
        print(f"       Title: {doc.metadata.get('title')}")
        print(f"       Content: {doc.page_content[:100]}...")

def check_vector_db():
    """벡터 DB 확인"""
    print("\n" + "=" * 80)
    print("벡터 DB 확인")
    print("=" * 80)
    
    try:
        vector_db = initialize_vector_db()
        
        # 각 놀이터로 검색 테스트
        zones = ["AI놀이터", "탐구놀이터", "관찰놀이터", "행동놀이터"]
        
        for zone in zones:
            print(f"\n🔍 '{zone}' 검색 결과:")
            docs = vector_db.similarity_search(zone, k=5)
            print(f"   검색된 문서 수: {len(docs)}")
            
            for i, doc in enumerate(docs[:3]):
                category = doc.metadata.get('category', 'N/A')
                title = doc.metadata.get('title', 'N/A')
                match = "✅" if zone in category else "❌"
                print(f"   [{i+1}] {match} Category: {category}, Title: {title}")
                
    except Exception as e:
        print(f"❌ 벡터 DB 오류: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_csv_files()
    check_loaded_docs()
    check_vector_db()
    
    print("\n" + "=" * 80)
    print("디버깅 완료")
    print("=" * 80)
