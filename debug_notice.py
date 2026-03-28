import requests
from bs4 import BeautifulSoup
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

url = "https://www.csc.go.kr/boardList.do?bbspkid=22&type=N&page=1"

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
}

session = requests.Session()
session.headers.update(headers)

response = session.get(url, timeout=20, verify=False)
response.encoding = 'utf-8'

print(f"Status: {response.status_code}")
print(f"Content length: {len(response.text)}")

soup = BeautifulSoup(response.text, 'html.parser')

# 페이지 제목
print(f"\nPage title: {soup.title.string if soup.title else 'No title'}")

# 공지사항 관련 요소 찾기
print("\n=== Looking for notice elements ===")

# 1. table 구조 확인
tables = soup.find_all('table')
print(f"Tables found: {len(tables)}")
for i, table in enumerate(tables[:3]):
    print(f"  Table {i} classes: {table.get('class')}")
    rows = table.find_all('tr')
    print(f"  Table {i} rows: {len(rows)}")

# 2. ul 구조 확인
uls = soup.find_all('ul')
print(f"\nULs found: {len(uls)}")
for i, ul in enumerate(uls[:5]):
    print(f"  UL {i} classes: {ul.get('class')}")
    lis = ul.find_all('li', recursive=False)
    print(f"  UL {i} direct li children: {len(lis)}")

# 3. 특정 클래스 검색
print("\n=== Searching for specific classes ===")
rbbs = soup.find_all(class_=lambda x: x and 'rbbs' in ' '.join(x))
print(f"Elements with 'rbbs' in class: {len(rbbs)}")
for elem in rbbs[:3]:
    print(f"  {elem.name} - {elem.get('class')}")

board = soup.find_all(class_=lambda x: x and 'board' in ' '.join(x))
print(f"Elements with 'board' in class: {len(board)}")
for elem in board[:3]:
    print(f"  {elem.name} - {elem.get('class')}")

# 4. HTML 샘플 출력
print("\n=== HTML Sample (first 2000 chars) ===")
print(response.text[:2000])
