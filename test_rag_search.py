# test_rag_search.py - RAG 검색 테스트
from rag import initialize_vector_db

print("벡터 DB 초기화 중...")
vector_db = initialize_vector_db()

print("\n" + "=" * 80)
print("놀이터별 검색 테스트")
print("=" * 80)

zones = ["AI놀이터", "탐구놀이터", "관찰놀이터", "행동놀이터"]

for zone in zones:
    print(f"\n🔍 '{zone}' 검색:")
    docs = vector_db.similarity_search(zone, k=10)
    
    # 해당 놀이터 문서만 필터링
    zone_docs = [doc for doc in docs if zone in doc.metadata.get('category', '')]
    
    print(f"   전체 검색 결과: {len(docs)}개")
    print(f"   {zone} 문서: {len(zone_docs)}개")
    
    if zone_docs:
        print(f"\n   샘플 문서 (처음 3개):")
        for i, doc in enumerate(zone_docs[:3]):
            title = doc.metadata.get('title', 'N/A')
            category = doc.metadata.get('category', 'N/A')
            print(f"   [{i+1}] {title} (Category: {category})")
    else:
        print(f"   ⚠️ {zone} 문서를 찾을 수 없습니다!")

print("\n" + "=" * 80)
print("테스트 완료")
print("=" * 80)
