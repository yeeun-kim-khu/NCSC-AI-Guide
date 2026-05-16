import glob
import os

pages_dir = r"c:\Users\yeeun\Documents\Space Research\code\2026\0406\data\pages"

# URL mapping based on file names
url_mapping = {
    "탐구놀이터": "https://www.sciencecenter.go.kr/csc/exhibition-hall/permanent",
    "행동놀이터": "https://www.sciencecenter.go.kr/csc/exhibition-hall/permanent",
    "관찰놀이터": "https://www.sciencecenter.go.kr/csc/exhibition-hall/permanent",
    "생각놀이터": "https://www.sciencecenter.go.kr/csc/exhibition-hall/permanent",
    "AI놀이터": "https://www.sciencecenter.go.kr/csc/exhibition-hall/permanent",
    "천체투영관": "https://www.sciencecenter.go.kr/csc/exhibition-hall/planetarium",
    "천체관측소": "https://www.sciencecenter.go.kr/csc/exhibition-hall/observatory",
    "메타버스과학관": "https://www.sciencecenter.go.kr/csc/exhibition-hall/metaverse",
    "인사말": "https://www.sciencecenter.go.kr/csc/intro/greeting",
    "연혁": "https://www.sciencecenter.go.kr/csc/intro/history",
    "조직도": "https://www.sciencecenter.go.kr/csc/intro/organization",
    "시설안내": "https://www.sciencecenter.go.kr/csc/intro/facility",
    "이용안내": "https://www.sciencecenter.go.kr/csc/intro/usage",
    "오시는길": "https://www.sciencecenter.go.kr/csc/intro/location",
    "교통안내": "https://www.sciencecenter.go.kr/csc/intro/location",
    "자주묻는질문": "https://www.sciencecenter.go.kr/csc/intro/faq",
    "예약안내": "https://www.sciencecenter.go.kr/csc/reserve/reserve-guide",
    "개인예약": "https://www.sciencecenter.go.kr/csc/reserve/personal",
    "단체예약": "https://www.sciencecenter.go.kr/csc/reserve/group",
    "교육예약": "https://www.sciencecenter.go.kr/csc/reserve/edu-reserve",
    "과학교육실": "https://www.sciencecenter.go.kr/csc/science-edu/edu-room",
    "과학쇼": "https://www.sciencecenter.go.kr/csc/cultural-event/science-show",
    "전시해설": "https://www.sciencecenter.go.kr/csc/cultural-event/docent",
    "창작교실1": "https://www.sciencecenter.go.kr/csc/science-edu/edu-room",
    "창작교실2": "https://www.sciencecenter.go.kr/csc/science-edu/edu-room",
    "창작교실3": "https://www.sciencecenter.go.kr/csc/science-edu/edu-room",
    "창작교실4": "https://www.sciencecenter.go.kr/csc/science-edu/edu-room",
    "어린이교실": "https://www.sciencecenter.go.kr/csc/science-edu/edu-room",
    "홈페이지": "https://www.sciencecenter.go.kr/csc/index.do",
}

for filepath in glob.glob(os.path.join(pages_dir, "*.csv")):
    filename = os.path.basename(filepath)
    page_key = filename.replace(".csv", "")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace old domain with new domain for all files
    new_content = content.replace('www.csc.go.kr', 'www.sciencecenter.go.kr')
    
    # Also replace specific old paths with new paths
    for key, new_url in url_mapping.items():
        if key in filename:
            # Replace all old URLs with the new one
            lines = new_content.split('\n')
            new_lines = []
            for line in lines:
                if line.startswith(f"{key},https://"):
                    parts = line.split(',')
                    if len(parts) >= 2:
                        parts[1] = new_url
                        new_lines.append(','.join(parts))
                    else:
                        new_lines.append(line)
                else:
                    new_lines.append(line)
            new_content = '\n'.join(new_lines)
            break
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"Updated: {filename}")

print("Done!")
