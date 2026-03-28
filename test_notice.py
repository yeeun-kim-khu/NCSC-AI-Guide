import requests
from bs4 import BeautifulSoup
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = "https://www.csc.go.kr/boardList.do?bbspkid=22&type=N&page=1"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
}

session = requests.Session()
session.headers.update(headers)

try:
    response = session.get(url, timeout=20, verify=False)
    response.encoding = 'utf-8'
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    print("=== HTML 구조 분석 ===")
    print(f"Response status: {response.status_code}")
    print(f"Response length: {len(response.text)}")
    
    # 다양한 선택자 시도
    selectors = [
        ".rbbs_list_thumb_sec ul li",
        "ul.board_list li",
        ".board_list li",
        "table.board_list tbody tr",
        ".notice_list li",
        "div[class*='list'] li",
        "ul li"
    ]
    
    for selector in selectors:
        items = soup.select(selector)
        print(f"\n{selector}: {len(items)} items")
        if items:
            print(f"First item classes: {items[0].get('class')}")
            print(f"First item text preview: {items[0].get_text(strip=True)[:100]}")
    
    # 모든 div 클래스 출력
    print("\n=== All div classes ===")
    divs = soup.find_all('div', class_=True)
    unique_classes = set()
    for div in divs:
        classes = div.get('class')
        if classes:
            unique_classes.update(classes)
    
    for cls in sorted(unique_classes):
        if 'list' in cls.lower() or 'board' in cls.lower():
            print(f"- {cls}")
    
    # HTML 일부 저장
    with open('notice_html_sample.html', 'w', encoding='utf-8') as f:
        f.write(response.text[:10000])
    print("\n✅ HTML 샘플 저장: notice_html_sample.html")
    
except Exception as e:
    print(f"❌ Error: {e}")
