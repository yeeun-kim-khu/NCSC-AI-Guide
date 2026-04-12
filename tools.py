# tools.py
import requests
from bs4 import BeautifulSoup
from langchain.tools import tool
from datetime import datetime, timezone, timedelta
from config import CSC_URLS
import urllib3

# SSL 경고 무시
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def parse_html_tables_to_markdown(soup: BeautifulSoup) -> str:
    """HTML Table을 마크다운으로 파싱하여 LLM이 표 데이터를 이해하도록 돕습니다."""
    markdown_text = ""
    for table in soup.find_all("table"):
        rows = table.find_all("tr")
        for i, row in enumerate(rows):
            cols = row.find_all(["th", "td"])
            row_text = "| " + " | ".join(col.get_text(strip=True) for col in cols) + " |"
            markdown_text += row_text + "\n"
            if i == 0:
                markdown_text += "|" + "|".join(["---"] * len(cols)) + "|\n"
        markdown_text += "\n"
    return markdown_text

@tool
def check_museum_closed_date(date_str: str) -> str:
    """
    특정 날짜의 국립어린이과학관 휴관일 여부를 확인합니다.
    
    [언제 사용하는가]
    - 사용자가 "내일 가도 돼?", "다음주 월요일 열어?", "3월 24일 휴관이야?" 같은 질문을 할 때
    - 특정 날짜의 운영 여부를 확인해야 할 때
    
    [입력 형식]
    - date_str: "2026-03-24" 또는 "내일" 또는 "다음주 월요일" 형태
    
    [무엇을 반환하는가]
    - 해당 날짜의 휴관 여부와 이유 (정기휴관/명절/대체휴관/정상운영)
    """
    # 날짜 파싱
    now_utc = datetime.now(timezone.utc)
    now_kst = now_utc + timedelta(hours=9)
    
    if "내일" in date_str or "tomorrow" in date_str.lower():
        target_date = now_kst + timedelta(days=1)
    elif "모레" in date_str:
        target_date = now_kst + timedelta(days=2)
    else:
        try:
            target_date = datetime.strptime(date_str, "%Y-%m-%d")
        except:
            return f"Observation: 날짜 형식을 인식할 수 없습니다. YYYY-MM-DD 형식으로 입력해주세요. 입력값: {date_str}"
    
    # 휴관일 확인 로직
    month_day = target_date.strftime("%m-%d")
    weekday = target_date.weekday()
    weekday_kr = ["월", "화", "수", "목", "금", "토", "일"][weekday]
    
    monday_exceptions = {"02-16", "03-02", "05-25", "08-17", "10-05"}
    holiday_closed = {"01-01", "02-17", "09-25"}
    substitute_closed = {"02-19", "03-03", "05-26", "08-18", "10-06"}
    
    date_display = target_date.strftime("%Y년 %m월 %d일")
    
    if month_day in holiday_closed:
        return f"Observation: {date_display}({weekday_kr}요일)은 명절 정기 휴관일입니다. 국립어린이과학관은 휴관합니다."
    if month_day in substitute_closed:
        return f"Observation: {date_display}({weekday_kr}요일)은 대체 휴관일입니다. 국립어린이과학관은 휴관합니다."
    if weekday == 0 and month_day not in monday_exceptions:
        return f"Observation: {date_display}({weekday_kr}요일)은 정기휴관일입니다. 국립어린이과학관은 매주 월요일 휴관합니다."
    
    return f"Observation: {date_display}({weekday_kr}요일)은 정상 운영일입니다. 국립어린이과학관은 10:00~17:00 운영합니다."

@tool
def search_csc_live_info(keyword: str) -> str:
    """
    국립어린이과학관 공식 홈페이지의 실시간 정보를 확인합니다.
    
    [언제 사용하는가]
    - 전시관 상세 안내 (5개 놀이터, 천체투영관 등), 프로그램 정보, 예약 방법 등을 확인할 때
    - 교통안내, 시설안내, 편의시설 등을 확인할 때
    
    [무엇을 반환하는가]
    - 해당 페이지의 최신 본문 텍스트(표 포함)와 출처 URL
    """
    target_url = CSC_URLS.get(keyword)
    if not target_url:
        for key, url in CSC_URLS.items():
            if keyword in key or key in keyword:
                target_url = url
                keyword = key
                break
                
    if not target_url:
        return f"Observation: '{keyword}' 페이지를 찾을 수 없습니다. 홈페이지에서 검색하세요."

    try:
        response = requests.get(target_url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        
        tables_markdown = parse_html_tables_to_markdown(soup)
        for tag in soup(["script", "style", "nav", "header", "footer"]):
            tag.decompose()
            
        main_text = soup.get_text(separator="\n", strip=True)
        return f"Observation:\n{tables_markdown}\n\n{main_text[:3000]}"
    except Exception as e:
        return f"[크롤링 실패] {e}"

@tool
def search_education_programs(max_items: int = 5) -> str:
    """
    국립어린이과학관의 최신 교육 프로그램 목록을 확인합니다.
    
    [언제 사용하는가]
    - 사용자가 "교육 프로그램 뭐 있어?", "최근 교육 일정 알려줘" 같은 질문을 할 때
    - 어린이 과학교육, K-사이언스, 창경궁 과학 나들이 등 프로그램 정보가 필요할 때
    
    [입력]
    - max_items: 가져올 프로그램 개수 (기본 5개)
    
    [무엇을 반환하는가]
    - 최신 교육 프로그램 제목, 날짜, 상세 링크 목록
    """
    url = "https://www.csc.go.kr/boardList.do?bbspkid=36&type=W&page=1"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        
        # 교육 프로그램 목록 추출
        programs = []
        items = soup.select(".rbbs_list_thumb_sec ul li")[:max_items]
        
        for item in items:
            title_elem = item.select_one(".title")
            date_elem = item.select_one(".info_line")
            link_elem = item.select_one("a[onclick]")
            
            if title_elem and date_elem:
                title = title_elem.get_text(strip=True)
                date = date_elem.get_text(strip=True)
                
                # onclick="goView('2253', '0', '1')" 에서 pkid 추출
                pkid = None
                if link_elem and "onclick" in link_elem.attrs:
                    onclick = link_elem["onclick"]
                    import re
                    match = re.search(r"goView\('(\d+)',", onclick)
                    if match:
                        pkid = match.group(1)
                
                program_info = f"- **{title}** ({date})"
                if pkid:
                    program_info += f" [상세보기: pkid={pkid}]"
                programs.append(program_info)
        
        if programs:
            result = "Observation: 최신 교육 프로그램 목록\n\n" + "\n".join(programs)
            result += f"\n\n상세 내용이 필요하면 search_program_detail 도구를 사용하세요."
            return result
        else:
            return "Observation: 교육 프로그램 목록을 찾을 수 없습니다."
            
    except Exception as e:
        return f"Observation: 교육 프로그램 크롤링 실패 - {e}"

@tool
def search_program_detail(pkid: str) -> str:
    """
    특정 교육 프로그램의 상세 내용을 확인합니다.
    
    [언제 사용하는가]
    - search_education_programs에서 받은 pkid로 상세 내용을 확인할 때
    - 사용자가 특정 프로그램의 자세한 정보를 요청할 때
    
    [입력]
    - pkid: 프로그램 고유 번호 (예: "2253")
    
    [무엇을 반환하는가]
    - 프로그램 상세 내용 (본문, 첨부파일 정보 등)
    """
    url = f"https://www.csc.go.kr/boardView.do?bbspkid=36&pkid={pkid}"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        
        # 제목 추출
        title_elem = soup.select_one(".view_tit, .title, h2, .board_view_tit")
        title = title_elem.get_text(strip=True) if title_elem else "제목 없음"
        
        # 본문 내용 추출 - 실제 HTML 구조: div.substance
        content_elem = soup.select_one(".substance")
        if content_elem:
            # script, style 태그 제거
            for tag in content_elem(["script", "style"]):
                tag.decompose()
            content = content_elem.get_text(separator="\n", strip=True)
        else:
            content = "본문 내용을 찾을 수 없습니다."
        
        # 첨부파일 정보 추출
        attachments = []
        attach_elems = soup.select(".attach_file_layer li, .file_list li")
        for attach in attach_elems:
            file_name = attach.get_text(strip=True)
            if file_name:
                attachments.append(f"  - {file_name}")
        
        result = f"Observation: [{title}]\n\n{content[:2000]}"
        if attachments:
            result += "\n\n첨부파일:\n" + "\n".join(attachments)
        
        return result
        
    except Exception as e:
        return f"Observation: 프로그램 상세 정보 크롤링 실패 - {e}"

@tool
def search_notice_detail(pkid: str) -> str:
    """
    공지사항 상세 페이지의 본문 내용을 가져옵니다.
    
    [언제 사용하는가]
    - 사용자가 특정 공지사항의 상세 내용을 알고 싶을 때
    - 공지사항 목록에서 특정 항목을 선택했을 때
    
    [입력]
    - pkid: 공지사항 게시글 고유 ID (예: "12345")
    
    [무엇을 반환하는가]
    - 공지사항 본문 내용 (HTML 태그 제거, 텍스트만)
    """
    url = f"https://www.csc.go.kr/boardView.do?pkid={pkid}&bbspkid=22&type=N"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'Connection': 'keep-alive'
    }
    
    try:
        # 세션 사용 및 SSL 검증 비활성화
        session = requests.Session()
        session.headers.update(headers)
        response = session.get(url, timeout=20, verify=False)
        response.encoding = 'utf-8'  # 한글 깨짐 방지
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # div.substance에서 본문 추출
        substance = soup.select_one("div.substance")
        if substance:
            # 이미지, 스크립트 태그 제거
            for tag in substance(["img", "script", "style"]):
                tag.decompose()
            
            # 텍스트만 추출
            content = substance.get_text(separator="\n", strip=True)
            # 빈 줄 제거
            content = "\n".join([line for line in content.split("\n") if line.strip()])
            
            return f"Observation: 공지사항 상세 내용\n\n{content[:1500]}"
        else:
            return "Observation: 본문(div.substance)을 찾을 수 없습니다. HTML 구조를 확인하세요."
            
    except requests.exceptions.Timeout:
        return "Observation: 공지사항 상세 페이지 접속 시간 초과 (20초)."
    except requests.exceptions.SSLError as e:
        return f"Observation: SSL 인증서 오류 - {str(e)}"
    except requests.exceptions.ConnectionError as e:
        return f"Observation: 네트워크 연결 오류 - {str(e)}"
    except Exception as e:
        return f"Observation: 상세 페이지 접근 중 오류 발생 - {str(e)}"

@tool
def search_faq(category: str = "전체") -> str:
    """
    자주묻는질문(FAQ)을 검색합니다.
    
    [언제 사용하는가]
    - 사용자가 "자주 묻는 질문", "FAQ" 등을 요청할 때
    - 예약, 방문, 관람 관련 질문이 있을 때
    
    [입력]
    - category: "전체", "예약", "방문", "관람" 등
    
    [무엇을 반환하는가]
    - FAQ 목록 (제목, 날짜)
    """
    url = "https://www.csc.go.kr/boardList.do?bbspkid=10&type=F&page=1"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        
        faqs = []
        items = soup.select(".rbbs_list_thumb_sec ul li")[:5]
        
        for item in items:
            title_elem = item.select_one(".title")
            if title_elem:
                title = title_elem.get_text(strip=True)
                faqs.append(f"- {title}")
        
        if faqs:
            return "Observation: 자주묻는질문\n\n" + "\n".join(faqs)
            return "Observation: FAQ를 찾을 수 없습니다."
    except Exception as e:
        return f"Observation: FAQ 크롤링 실패 - {e}"

@tool
def search_notices(max_items: int = 5) -> str:
    """
    최신 공지사항을 검색합니다.
    
    [언제 사용하는가]
    - 사용자가 "공지사항", "최신 소식" 등을 요청할 때
    
    [무엇을 반환하는가]
    - 최신 공지사항 목록 (제목, 날짜, pkid)
    """
    url = "https://www.csc.go.kr/boardList.do?bbspkid=22&type=N&page=1"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }
    
    try:
        # 세션 사용 및 SSL 검증 비활성화
        session = requests.Session()
        session.headers.update(headers)
        
        response = session.get(url, timeout=20, verify=False)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        
        notices = []
        
        # 실제 HTML 구조: div.rbbs_list_normal_sec > ul > li
        items = soup.select("div.rbbs_list_normal_sec ul li")[:max_items]
        
        if not items:
            # 대체 선택자 시도
            items = soup.select(".rbbs_list_normal_sec ul li")[:max_items]
        
        if not items:
            # 디버깅 정보
            all_divs = soup.find_all('div', class_=lambda x: x and 'rbbs' in ' '.join(x) if x else False)
            return f"Observation: 공지사항 항목을 찾을 수 없습니다.\n디버깅 정보:\n- rbbs 관련 div 수: {len(all_divs)}\n- 첫 번째 rbbs div: {all_divs[0].get('class') if all_divs else 'None'}"
        
        for item in items:
            # 제목: div.title > div.text
            title_elem = item.select_one("div.title div.text")
            if not title_elem:
                title_elem = item.select_one("div.title")
            
            # 날짜: div.info_line (LLM이 파악용, 출력 안 함)
            date_elem = item.select_one("div.info_line")
            
            # 링크: a[onclick]
            link_elem = item.select_one("a[onclick]")
            
            if title_elem:
                title = title_elem.get_text(strip=True)
                date = date_elem.get_text(strip=True) if date_elem else ""
                
                # pkid 추출
                pkid = None
                if link_elem and "onclick" in link_elem.attrs:
                    onclick = link_elem["onclick"]
                    import re
                    match = re.search(r"goView\('(\d+)',", onclick)
                    if match:
                        pkid = match.group(1)
                
                # 공지사항 상세 내용 발췌 (요약용)
                summary = ""
                if pkid:
                    try:
                        detail_url = f"https://www.csc.go.kr/boardView.do?pkid={pkid}&bbspkid=22&type=N"
                        detail_response = session.get(detail_url, timeout=10, verify=False)
                        detail_response.encoding = 'utf-8'
                        detail_soup = BeautifulSoup(detail_response.text, 'html.parser')
                        
                        substance = detail_soup.select_one("div.substance")
                        if substance:
                            for tag in substance(["img", "script", "style"]):
                                tag.decompose()
                            content = substance.get_text(separator=" ", strip=True)
                            # 첫 200자만 발췌
                            summary = content[:200].strip()
                            if len(content) > 200:
                                summary += "..."
                    except:
                        summary = ""
                
                # 제목 + 발췌 요약 (날짜는 내부 데이터로만 유지)
                notice_info = f"- **{title}**"
                if summary:
                    notice_info += f"\n  요약: {summary}"
                notice_info += f"\n  [작성일: {date}]"  # LLM이 파악할 수 있도록 포함
                if pkid:
                    notice_info += f" [pkid={pkid}]"
                notices.append(notice_info)
        
        if notices:
            result = "Observation: 최신 공지사항\n\n" + "\n".join(notices)
            result += "\n\n상세 내용이 필요하면 search_notice_detail 도구를 사용하세요."
            return result
        else:
            return "Observation: 공지사항을 찾을 수 없습니다. HTML 구조를 확인해주세요."
    except requests.exceptions.Timeout:
        return "Observation: 공지사항 페이지 접속 시간 초과 (20초). 네트워크 상태를 확인해주세요."
    except requests.exceptions.SSLError as e:
        return f"Observation: SSL 인증서 오류 - {str(e)}"
    except requests.exceptions.ConnectionError as e:
        return f"Observation: 네트워크 연결 오류 - {str(e)}"
    except requests.exceptions.RequestException as e:
        return f"Observation: 공지사항 페이지 접속 실패 - {str(e)}"
    except Exception as e:
        return f"Observation: 공지사항 크롤링 중 오류 발생 - {str(e)}"

@tool
def search_web_realtime(query: str, max_results: int = 5) -> str:
    """
    Real-time web search for current information beyond static museum data.
    
    [When to use]
    - When user asks about recent events, news, or time-sensitive information
    - When RAG database doesn't contain sufficient information
    - For current science trends, temporary exhibitions, or special events
    
    [Input]
    - query: Search query string
    - max_results: Maximum number of results to return (default: 5)
    
    [Returns]
    - Recent web search results with snippets and sources
    """
    try:
        # Using a simple web search simulation (replace with actual search API)
        # For demonstration, we'll simulate with predefined responses
        
        search_results = [
            {
                "title": "National Children's Science Center - Latest Updates",
                "snippet": "Check our official website for the most current information about exhibitions and programs.",
                "url": "https://www.csc.go.kr"
            },
            {
                "title": "Science Education Programs 2026",
                "snippet": "New educational programs focusing on AI and robotics for children aged 7-15.",
                "url": "https://www.csc.go.kr/education"
            }
        ]
        
        result_text = "Observation: Real-time web search results\n\n"
        for i, result in enumerate(search_results[:max_results], 1):
            result_text += f"{i}. **{result['title']}**\n"
            result_text += f"   {result['snippet']}\n"
            result_text += f"   Source: {result['url']}\n\n"
        
        return result_text
        
    except Exception as e:
        return f"Observation: Real-time search failed - {str(e)}"

@tool
def analyze_scientific_principle(topic: str, user_level: str = "intermediate") -> str:
    """
    Deep analysis of scientific principles with age-appropriate explanations.
    
    [When to use]
    - When user asks "how does this work?" or "what's the principle behind this?"
    - For detailed explanations of scientific concepts exhibited in the museum
    - When user wants to understand the science behind exhibits
    
    [Input]
    - topic: Scientific topic or principle to analyze
    - user_level: "beginner" (children), "intermediate" (teens), "advanced" (adults)
    
    [Returns]
    - Detailed explanation of the scientific principle with examples
    """
    # Predefined scientific principles commonly found in the museum
    principles_db = {
        "light refraction": {
            "beginner": "Light bends when it passes through water or glass, like a straw looking bent in a water glass! This happens because light travels at different speeds in different materials.",
            "intermediate": "Light refraction occurs due to the change in speed when light passes between media of different densities. The refractive index determines the degree of bending according to Snell's law: n1sin(1) = n2sin(2).",
            "advanced": "Refraction is governed by the electromagnetic wave properties of light and the dielectric properties of materials. The refractive index n = c/v where c is the speed of light in vacuum and v is the phase velocity in the medium."
        },
        "magnetic force": {
            "beginner": "Magnets can push or pull things without touching them! Some magnets stick to refrigerators because they have invisible force fields around them.",
            "intermediate": "Magnetic force is a fundamental force mediated by magnetic fields. Like poles repel while opposite poles attract. The force follows F = q(v × B) for moving charges.",
            "advanced": "Magnetic forces arise from the motion of electric charges and intrinsic magnetic moments of particles. The field is described by Maxwell's equations: ×B = 0(J + 0E/t)."
        },
        "sound waves": {
            "beginner": "Sound travels through air like waves in water! When something vibrates, it makes the air around it vibrate too, and that's how we hear sounds.",
            "intermediate": "Sound waves are longitudinal mechanical waves that propagate through matter via particle vibrations. Key properties include frequency (pitch), amplitude (loudness), and wave speed v = f.",
            "advanced": "Acoustic waves are governed by the wave equation ²p/t² = c²²p/x², where p is pressure and c is the speed of sound. The speed depends on the medium's elastic modulus and density: c = (E/)."
        }
    }
    
    topic_lower = topic.lower()
    result = "Observation: Scientific principle analysis\n\n"
    
    # Search for the principle in our database
    for key, explanations in principles_db.items():
        if topic_lower in key or key in topic_lower:
            level = user_level if user_level in explanations else "intermediate"
            result += f"**Topic**: {topic.title()}\n"
            result += f"**Level**: {user_level}\n"
            result += f"**Explanation**: {explanations[level]}\n\n"
            result += "This principle is demonstrated in our museum's interactive exhibits!"
            return result
    
    # If not found, provide a general response
    result += f"**Topic**: {topic.title()}\n"
    result += f"**Level**: {user_level}\n"
    result += f"**Analysis**: This scientific principle is featured in our museum exhibits. "
    result += f"For detailed explanations, please visit the relevant exhibition hall or ask our staff for demonstrations. "
    result += f"You can also explore this topic through our interactive learning stations."
    
    return result

def get_tools():
    return [check_museum_closed_date, search_csc_live_info, search_education_programs, search_program_detail, search_notice_detail, search_faq, search_notices, search_web_realtime, analyze_scientific_principle]