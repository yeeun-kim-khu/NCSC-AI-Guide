# config.py - 모든 설정과 규칙을 한 곳에 통합
# (constants.py + rules.py 통합)

import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo

# ============================================================================
# CONSTANTS - 상수 정의
# ============================================================================

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

# RAG vector DB core data (LLM reference)
STATIC_EXHIBIT_INFO = {
    # Exhibition zones - detailed info from CSV files only
    "탐구놀이터": """탐구놀이터는 생활 속 도구, 에너지, 기계 등의 작동원리를 관찰하고 체험해 보면서 탐구해보는 체험 공간입니다.
위치: 2층
상세 전시물 정보는 CSV 데이터를 참조하세요.""",
    
    "관찰놀이터": """관찰놀이터는 공룡, 화석, 표본 등을 디지털 미디어를 통해 관찰해보며 과학적 사고력을 키워보는 공간입니다.
위치: 2층
상세 전시물 정보는 CSV 데이터를 참조하세요.""",
    
    "AI놀이터": """AI놀이터는 인공지능 "조이"를 도와 지구를 지키기 위한 활동을 체험하는 공간입니다.
위치: 1층
상세 전시물 정보는 CSV 데이터를 참조하세요.""",
    
    "행동놀이터": """행동놀이터는 다양한 신체 활동을 통해 내 몸을 알아보고 건강한 어린이가 되어보는 공간입니다.
위치: 1층
상세 전시물 정보는 CSV 데이터를 참조하세요.""",
    
    "생각놀이터": """생각놀이터는 어린이들의 생각을 키울 전시관으로, 2026년 5월 개관을 앞두고 있습니다.
위치: 1층""",
    
    "빛놀이터": """빛놀이터는 씨앗이 자라 나무가 되고, 나무들이 숲을 만드는 과정과 생태계 상호작용의 과학적 원리를 미디어 인터랙션을 통해 체험해 볼 수 있는 몰입형 실감 미디어 체험관입니다.
위치: 2층""",
    
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
관람시간: 오전 09:30 ~ 오후 17:30
입장마감: 오후 16:30
휴관일: 매주 월요일, 1월 1일, 설날/추석 당일
- 월요일이 공휴일인 경우 개관하며, 화요일에 대체 휴관
문의: 02-3668-1500

관람 시 유의사항:
- 전시관내 음식물 반입금지
- 애완동물 출입금지 (시각장애 안내견 제외)
- 바퀴달린 신발 착용금지
- 킥보드 탑승금지
- 뛰거나 큰소리로 떠들지 않기
- 체험시설물은 질서 있게 이용

관람방법:
- 어린이를 동반하지 않은 관람객 및 보호자를 동반하지 않은 어린이의 입장 제한
- 온라인 사전예약제 운영
- 과학관 입구(2층)에서 예약한 입장권(QR코드) 확인 후 관람
- 당일에 한해 입장권 소지 시 재입장 가능
- 상설전시관은 입장시간보다 늦을 경우에도 입장 가능""",
    
    "입장료": """국립어린이과학관 입장료
모든 나이는 '연나이' 기준 (연나이=현재년도-출생년도)

상설전시관:
- 성인(19세 이상): 개인 2,000원 (단체 이용불가)
- 청소년(13~18세): 개인 1,000원 (단체 이용불가)
- 초등학생(7~12세): 개인 1,000원 / 단체 500원
- 유아(6세 이하): 무료
- 우대고객: 무료 (65세 이상, 장애인, 과학기술유공자, 국가유공자, 기초생활수급자, 차상위계층, 한부모가족 지원대상자)

천체투영관:
- 성인(19세 이상): 1,500원
- 청소년(13~18세): 1,000원
- 초등학생(7~12세): 1,000원
- 유아(4~6세): 1,000원 (성인보호자 동반 및 결제시 이용 가능)
- 우대고객: 1,000원

할인 및 면제:
- 중증장애인(1~3급): 장애인과 동반보호자 1인 무료/우대요금
- 경증장애인(4급 이상): 장애인 본인만 무료/우대요금
- 다자녀카드 보유자: 상설전시관 개인요금의 50% 할인
- 단체 인솔자: 초등학생 20명당 1명, 유아 10명당 1명 무료

유의사항:
- 어린이를 동반하지 않은 성인 및 청소년, 보호자를 동반하지 않은 9세 이하 어린이 입장 제한
- 개인 관람객 환불은 관람 당일 오전 10시 전까지 신청콕에서 전체 취소만 가능
- 우대고객은 신분증과 증명서 지참 필수""",
    
    "교통안내": """국립어린이과학관 오시는 길
- 주소: 서울특별시 종로구 창경궁로 215
- 지하철: 4호선 혜화역 4번 출구 도보 10분
- 버스: 파랑(간선) 100, 102, 104, 106, 107, 108, 140, 143, 150, 160, 163, 172, 273, 710 / 초록(지선) 2112""",
    
    "예약안내": """국립어린이과학관 예약 방법
- 개인 예약: 홈페이지에서 관람일 7일 전부터 예약 가능
- 단체 예약: 20인 이상, 관람일 14일 전까지 예약 필수
- 교육 프로그램: 각 프로그램별 공지사항 확인 후 예약
- 천체투영관: 사전 예약 필수 (현장 예약 불가)
- 예약 취소: 관람일 1일 전까지 가능
- 문의: 02-3668-1500"""
}

# ============================================================================
# RULES - 규칙 및 로직 함수
# ============================================================================

def route_intent(text: str) -> str:
    """사용자 질문의 의도를 파악하여 라우팅"""
    lowered = text.lower().strip()
    # 공지사항은 LLM이 처리 (search_notices, search_notice_detail 도구 사용)
    if any(token in lowered for token in ["운영", "시간", "휴관", "입장료", "관람료", "주차"]):
        return "basic"
    return "llm_agent"

def classify_basic_category(message: str) -> str:
    """기본 질문 카테고리 분류"""
    lowered = message.lower()
    rules = [
        ("operating_hours", ["운영", "시간", "휴관", "몇 시", "마감"]),
        ("admission_fee",   ["관람료", "입장료", "요금", "가격", "얼마"]),
        ("parking",         ["주차", "주차장"]),
    ]
    for category, keywords in rules:
        if any(keyword in lowered for keyword in keywords):
            return category
    return "operating_hours"

def check_closed_date(target_date: datetime) -> tuple[bool, str]:
    """특정 날짜의 휴관 여부 확인"""
    month_day = target_date.strftime("%m-%d")
    weekday = target_date.weekday()
    weekday_kr = ["월", "화", "수", "목", "금", "토", "일"][weekday]
    
    monday_exceptions = {"02-16", "03-02", "05-25", "08-17", "10-05"}
    holiday_closed = {"01-01", "02-17", "09-25"}
    substitute_closed = {"02-19", "03-03", "05-26", "08-18", "10-06"}
    
    if month_day in holiday_closed:
        return (True, f"{target_date.strftime('%m월 %d일')}({weekday_kr}요일)은 명절 정기 휴관일입니다.")
    if month_day in substitute_closed:
        return (True, f"{target_date.strftime('%m월 %d일')}({weekday_kr}요일)은 대체 휴관일입니다.")
    if weekday == 0 and month_day not in monday_exceptions:
        return (True, f"{target_date.strftime('%m월 %d일')}({weekday_kr}요일)은 정기휴관일(월요일)입니다.")
    
    return (False, f"{target_date.strftime('%m월 %d일')}({weekday_kr}요일)은 정상 운영일입니다.")

def get_today_status() -> str:
    """오늘 과학관 운영 상태 확인"""
    now_utc = datetime.now(timezone.utc)
    now = now_utc + timedelta(hours=9)  # KST = UTC+9
    is_closed, status_msg = check_closed_date(now)
    
    if is_closed:
        return status_msg
    
    current = now.time()
    if current.hour < 10:
        return "아직 개관 전이에요. (운영시간: 10:00~17:00)"
    if current.hour >= 17:
        return "오늘 운영 시간은 종료됐어요. (운영시간: 10:00~17:00)"
    return "현재 정상 운영 중입니다! (운영시간: 10:00~17:00)"

def answer_rule_based(intent: str, message: str, mode: str) -> str:
    """규칙 기반 답변 생성"""
    # 공지사항은 LLM이 처리 (search_notices, search_notice_detail 도구 사용)
    
    if intent == "basic":
        category = classify_basic_category(message)
        if category == "operating_hours":
            status = get_today_status()
            prefix = "오늘 어린이과학관은 어떨까요? 🚀\n" if mode == "어린이" else "운영 상태 안내입니다.\n"
            return f"{prefix}\n{status}"
        elif category == "admission_fee":
            fee_table = """
| 대상 | 연령/구분 | 개인 | 단체(20인 이상) |
| --- | --- | ---: | ---: |
| 어른 | 20~64세 | 2,000원 | 1,000원 |
| 청소년/어린이 | 7~19세 | 1,000원 | 500원 |
| 무료 | 6세 이하, 65세 이상 | 무료 | 무료 |
"""
            prefix = "상설전시관 관람료를 알려드릴게요! 💸\n" if mode == "어린이" else "상설전시관 관람료 안내입니다.\n"
            return f"{prefix}{fee_table}"
        elif category == "parking":
            return ""
            
    return ""
