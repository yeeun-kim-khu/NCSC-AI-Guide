# constants.py
MUSEUM_BASE_URL = "https://www.csc.go.kr"

# 국립어린이과학관 주요 URL 맵
CSC_URLS = {
    # 홈페이지
    "홈페이지": f"{MUSEUM_BASE_URL}/index.do",
    
    # 과학관 소개
    "인사말": f"{MUSEUM_BASE_URL}/new1/introduce/introduce.jsp",
    "연혁": f"{MUSEUM_BASE_URL}/new1/introduce/overview.jsp",
    "조직도": f"{MUSEUM_BASE_URL}/new1/introduce/organization.jsp",
    "시설안내": f"{MUSEUM_BASE_URL}/new1/information/facility.jsp",
    
    # 관람안내
    "이용안내": f"{MUSEUM_BASE_URL}/new1/information/tourinfo.jsp",
    "오시는길": f"{MUSEUM_BASE_URL}/new1/information/direction.jsp",
    "교통안내": f"{MUSEUM_BASE_URL}/new1/information/direction.jsp",
    "자주묻는질문": f"{MUSEUM_BASE_URL}/boardList.do?bbspkid=10&type=F&page=1",
    
    # 예약
    "예약안내": f"{MUSEUM_BASE_URL}/new1/reservation/guide.jsp",
    "개인예약": f"{MUSEUM_BASE_URL}/new1/reservation/reservation_person.jsp",
    "단체예약": f"{MUSEUM_BASE_URL}/new1/reservation/reservation_group.jsp",
    "교육예약": f"{MUSEUM_BASE_URL}/new1/reservation/education_creation.jsp",
    
    # 전시관 - 상설전시관 (5개 놀이터)
    "탐구놀이터": f"{MUSEUM_BASE_URL}/new1/centers/exhibitinfo_1.jsp",
    "관찰놀이터": f"{MUSEUM_BASE_URL}/new1/centers/exhibitinfo_2.jsp",
    "행동놀이터": f"{MUSEUM_BASE_URL}/new1/centers/exhibitinfo_3.jsp",
    "생각놀이터": f"{MUSEUM_BASE_URL}/new1/centers/exhibitinfo_4.jsp",
    "AI놀이터": f"{MUSEUM_BASE_URL}/new1/centers/exhibitinfo_5.jsp",
    
    # 전시관 - 천문우주
    "천체투영관": f"{MUSEUM_BASE_URL}/new1/centers/space.jsp",
    "천체관측소": f"{MUSEUM_BASE_URL}/new1/centers/space_2.jsp",
    "메타버스과학관": f"{MUSEUM_BASE_URL}/new1/centers/metaverse.jsp",
    
    # 과학교육
    "과학교육실": f"{MUSEUM_BASE_URL}/new1/centers/ckdwkr.jsp",
    "창작교실1": f"{MUSEUM_BASE_URL}/new1/centers/exhibitinfo_49.jsp",
    "창작교실2": f"{MUSEUM_BASE_URL}/new1/centers/exhibitinfo_50.jsp",
    "창작교실3": f"{MUSEUM_BASE_URL}/new1/centers/exhibitinfo_51.jsp",
    "창작교실4": f"{MUSEUM_BASE_URL}/new1/centers/exhibitinfo_58.jsp",
    "어린이교실": f"{MUSEUM_BASE_URL}/new1/centers/exhibitinfo_59.jsp",
    
    # 문화행사
    "과학쇼": f"{MUSEUM_BASE_URL}/new1/centers/exhibitinfo_57.jsp",
    "전시해설": f"{MUSEUM_BASE_URL}/new1/centers/explanation.jsp",
}

# RAG 벡터 DB에 주입될 핵심 정적 데이터 (LLM이 답변할 때 참조)
STATIC_EXHIBIT_INFO = {
    # 상설전시관 (5개 놀이터)
    "탐구놀이터": """물, 빛, 소리 등 다양한 과학 현상을 직접 탐구하며 배우는 체험 공간입니다. 어린이들이 호기심을 가지고 자유롭게 실험할 수 있습니다.
주요 전시물: 물의 순환, 빛의 굴절, 소리의 진동, 자석의 힘, 전기 회로 등
대상: 유아~초등학생
특징: 자유 관람, 체험 중심, 과학 원리 학습""",
    
    "관찰놀이터": """자연과 생명을 관찰하며 과학적 사고력을 기르는 공간입니다. 동식물, 곤충 등을 관찰하고 탐구할 수 있습니다.
주요 전시물: 곤충 표본, 식물 관찰, 현미경 체험, 생태계 모형
대상: 유아~초등학생
특징: 살아있는 생물 관찰 가능, 자연 과학 학습""",
    
    "행동놀이터": """몸을 움직이며 과학 원리를 체험하는 신체 활동 중심 전시관입니다. 운동, 균형, 힘 등을 놀이로 배웁니다.
주요 전시물: 균형 잡기, 힘의 원리, 운동 에너지, 중력 체험
대상: 유아~초등학생
특징: 신체 활동 중심, 에너지 소비형 전시""",
    
    "생각놀이터": """창의적 사고와 문제 해결 능력을 키우는 공간입니다. 퍼즐, 게임 등을 통해 논리적 사고를 발달시킵니다.
주요 전시물: 논리 퍼즐, 수학 게임, 공간 지각 체험, 창의력 놀이
대상: 초등학생~중학생
특징: 사고력 향상, 문제 해결 중심""",
    
    "AI놀이터": """인공지능과 로봇 기술을 체험하며 미래 과학기술을 배우는 최신 전시 공간입니다. 코딩, AI 체험이 가능합니다.
주요 전시물: AI 챗봇, 로봇 프로그래밍, 코딩 게임, 자율주행 체험
대상: 초등학생~중학생
특징: 최신 기술 체험, 코딩 교육, 미래 직업 탐색""",
    
    # 천문우주 시설
    "천체투영관": """돔 스크린에서 별자리와 우주를 관람하는 곳입니다. 계절별 별자리 해설과 천문 영상을 상영합니다.
상영 시간: 평일 11시, 14시, 16시 / 주말 11시, 13시, 15시, 17시
소요 시간: 약 40분
예약: 홈페이지 사전 예약 필수 (현장 예약 불가)
특징: 전문 해설사의 별자리 설명, 계절별 다른 프로그램""",
    
    "천체관측소": """망원경으로 태양, 달, 행성 등을 직접 관측하는 공간입니다. 날씨에 따라 관측 가능 여부가 달라집니다.
관측 시간: 주간(태양 관측) 10시~17시, 야간(별 관측) 19시~21시
예약: 홈페이지 사전 예약 필수
주의사항: 날씨에 따라 관측 불가능할 수 있음
특징: 실제 천체 관측, 전문 망원경 사용""",
    
    "메타버스과학관": """가상현실(VR)로 과학관을 체험할 수 있는 온라인 공간입니다. 집에서도 전시관을 둘러볼 수 있습니다.
접속 방법: 국립어린이과학관 홈페이지 접속
이용 시간: 24시간 언제나 가능
특징: VR 기기 없이도 PC/모바일로 체험 가능, 전시관 가상 투어""",
    
    # 운영 정보
    "운영시간": """국립어린이과학관 운영시간
- 평일/주말: 10:00~17:00 (입장 마감 16:00)
- 휴관일: 매주 월요일 (단, 공휴일인 월요일은 개관하고 다음 평일 휴관)
- 명절 휴관: 설날, 추석 당일
- 문의: 02-3668-1500""",
    
    "입장료": """국립어린이과학관 입장료 (상설전시관 기준)
- 어른(20~64세): 개인 2,000원 / 단체(20인 이상) 1,000원
- 청소년/어린이(7~19세): 개인 1,000원 / 단체 500원
- 무료: 6세 이하, 65세 이상, 국가유공자, 장애인
- 천체투영관: 별도 요금 (어른 2,000원, 청소년/어린이 1,000원)
- 결제: 현장 카드/현금, 온라인 사전 결제 가능""",
    
    "교통안내": """국립어린이과학관 오시는 길
- 주소: 서울특별시 종로구 창경궁로 215
- 지하철: 4호선 혜화역 4번 출구 도보 10분
- 버스: 파랑(간선) 100, 102, 104, 106, 107, 108, 140, 143, 150, 160, 163, 172, 273, 710 / 초록(지선) 2112
- 주차: 과학관 지하 주차장 이용 가능 (유료, 30분 1,000원)
- 주차 할인: 과학관 이용 시 1시간 무료""",
    
    "예약안내": """국립어린이과학관 예약 방법
- 개인 예약: 홈페이지에서 관람일 7일 전부터 예약 가능
- 단체 예약: 20인 이상, 관람일 14일 전까지 예약 필수
- 교육 프로그램: 각 프로그램별 공지사항 확인 후 예약
- 천체투영관: 사전 예약 필수 (현장 예약 불가)
- 예약 취소: 관람일 1일 전까지 가능
- 문의: 02-3668-1500"""
}