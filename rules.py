# rules.py
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo
from constants import CSC_URLS

def route_intent(text: str) -> str:
    lowered = text.lower().strip()
    # 공지사항은 LLM이 처리 (search_notices, search_notice_detail 도구 사용)
    if any(token in lowered for token in ["운영", "시간", "휴관", "입장료", "관람료", "주차"]):
        return "basic"
    return "llm_agent"

def classify_basic_category(message: str) -> str:
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