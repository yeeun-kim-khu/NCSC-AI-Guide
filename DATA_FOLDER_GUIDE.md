# 데이터 폴더 구조 및 활용 가이드

> **목적**: `data/` 폴더와 `data/pages/` 폴더의 차이, 중복 여부, 각 파일의 용도를 명확히 설명

---

## 1. 폴더 구조 개요

```
data/
├── AI놀이터.csv          ← 전시물 상세 정보 (전시물품 대장)
├── 관찰놀이터.csv
├── 생각놀이터.csv
├── 행동놀이터.csv
├── 탐구놀이터널.csv
├── 천체투영관.csv
├── 공지사항.csv          ← 공지사항/교통안내/운영안내 등
├── 관람료.csv
├── 시설안내.csv
├── 예약안내.csv
├── 운영안내.csv
├── 교통안내.csv
├── 층별안내.csv
└── pages/                ← 홈페이지 크롤링 데이터
    ├── AI놀이터.csv      ← 홈페이지 전시안내 페이지 내용
    ├── 관찰놀이터.csv
    ├── 생각놀이터.csv
    ├── 행동놀이터.csv
    ├── 탐구놀이터.csv
    ├── 천체투영관.csv
    ├── 공지사항.csv      ← 홈페이지 공지사항 페이지
    ├── 교통안내.csv      ← 홈페이지 오시는길 페이지
    ├── 시설안내.csv      ← 홈페이지 시설안내 페이지
    ├── 예약안내.csv      ← 홈페이지 예약안내 페이지
    ├── 이용안내.csv      ← 홈페이지 이용안내 페이지
    ├── 홈페이지.csv      ← 메인 페이지 콘텐츠
    ├── 개인예약.csv      ← 홈페이지 개인예약 페이지
    ├── 단체예약.csv      ← 홈페이지 단체예약 페이지
    ├── 교육예약.csv      ← 홈페이지 교육예약 페이지
    ├── 전시해설.csv      ← 홈페이지 전시해설 프로그램 페이지
    ├── 과학쇼.csv        ← 홈페이지 과학쇼 프로그램 페이지
    ├── 과학교육실.csv    ← 홈페이지 과학교육실 페이지
    ├── 어린이교실.csv    ← 홈페이지 어린이교실 페이지
    ├── 창작교실1~4.csv   ← 홈페이지 창작교실 페이지
    ├── 천체관측소.csv    ← 홈페이지 천체관측소 페이지
    ├── 메타버스과학관.csv ← 홈페이지 메타버스과학관 페이지
    ├── 연혁.csv          ← 홈페이지 연혁 페이지
    ├── 조직도.csv        ← 홈페이지 조직도 페이지
    ├── 인사말.csv        ← 홈페이지 인사말 페이지
    ├── 자주묻는질문.csv  ← 홈페이지 FAQ 페이지
    └── 오시는길.csv      ← 홈페이지 오시는길 페이지
```

---

## 2. `data/` vs `data/pages/` 핵심 차이

| 항목 | `data/*.csv` | `data/pages/*.csv` |
|---|---|---|
| **데이터 출처** | 국립어린이과학관 **전시물품 대장** (엑셀 변환) | 과학관 **홈페이지 크롤링** (requests + BeautifulSoup) |
| **주요 컬럼** | `ID`, `분류`, `전시형태`, `작동방식`, `제목`, `내용`, `영문 내용`, `세부 설명` | `page_key`, `url`, `block_type`, `order`, `title`, `content` |
| **용도** | **RAG 벡터 DB** 구축, **또만나 놀이터** 전시물 정보 표시 | **규칙 기반 답변** 참조, **홈페이지 콘텐츠** 기반 FAQ |
| **데이터 품질** | 구조화된 전시물 정보, 영문 포함, 상세 설명 | 웹 페이지 그대로의 비정형 텍스트, 순서 정보 포함 |
| **파일 크기** | 큼 (AI놀이터: 15KB, 관찰놀이터: 41KB) | 작음 (AI놀이터: 1.6KB, 관찰놀이터: 1.8KB) |

---

## 3. 이름이 같은 파일들 비교

파일명이 같아도 **내용이 완전히 다름**. 중복이 아님.

### 예시: `data/AI놀이터.csv` vs `data/pages/AI놀이터.csv`

**`data/AI놀이터.csv`** (전시물품 대장)
```csv
ID,분류,전시형태,작동방식,제목,내용,영문 내용,세부 설명,영문 세부 설명,비고 및 주의사항,상태,영문,사진1,사진2
AI-0,개요,패널,텍스트,"인공지능 조이와 함께 지구를 지켜요","인간 활동이 만들어 낸 기후 위기로...","Our Earth is changing because of...",,,,정상,없음,,
AI-1,"지구가 아파요",패널,텍스트,"지구가 아파요","컴퓨터, 스마트폰, 자동차...","Computers, phones, cars...",,,,,,,
```
→ **각 전시물의 상세 설명, 영문 번역, 전시형태, 작동방식** 등이 포함된 구조화 데이터

**`data/pages/AI놀이터.csv`** (홈페이지 크롤링)
```csv
page_key,url,block_type,order,title,content
AI놀이터,https://www.csc.go.kr/new1/centers/exhibitinfo_5.jsp,text,0,,상설전시관
AI놀이터,https://www.csc.go.kr/new1/centers/exhibitinfo_5.jsp,text,1,,천체투영관
AI놀이터,https://www.csc.go.kr/new1/centers/exhibitinfo_5.jsp,text,4,"함께 만드는 우리의 미래",기후변화로 지구의 온도가 올라가면 우리는 어떻게 될까요?
```
→ **홈페이지의 섹션별 제목과 설명문**, URL, 페이지 내 순서 정보

### 예시: `data/공지사항.csv` vs `data/pages/공지사항.csv`

- `data/공지사항.csv`: 전시물품 대장의 "공지사항" 카테고리 (없거나 다른 내용)
- `data/pages/공지사항.csv`: 홈페이지 공지사항 게시글 목록 (제목, 날짜, 내용 요약)

---

## 4. 코드에서 각 폴더를 어떻게 사용하는가

### 4.1. RAG 벡터 DB 구축 (`core.py`)

```python
def load_csv_data() -> list[Document]:
    csv_files = glob.glob("data/*.csv") + glob.glob("data/pages/*.csv")
    for csv_file in csv_files:
        df = pd.read_csv(csv_file)
        # ... Document 객체로 변환하여 ChromaDB에 저장
```

- **두 폴더의 모든 CSV를 합쳐서** 벡터 DB(ChromaDB)를 구축
- `data/*.csv`의 풍부한 전시물 정보 + `data/pages/*.csv`의 홈페이지 콘텐츠를 모두 임베딩
- 질문 시 두 데이터 소스를 모두 검색하여 답변 생성

### 4.2. 규칙 기반 답변 (`core.py`)

```python
# answer_rule_based_localized() 내부
if intent == "operating_hours":
    rows = load_csv_data()  # data/pages/운영안내.csv 등에서 검색
```

- 규칙 기반 엔진은 주로 `data/pages/*.csv`의 **운영안내, 공지사항, 예약안내** 등을 참조
- 실시간으로 크롤링한 최신 정보가 `data/pages/`에 반영됨

### 4.3. 또만나 놀이터 전시물 로드 (`learning.py`)

```python
def load_zone_rows_from_csv(zone_name: str):
    # data/{zone_name}.csv 에서 전시물 목록 로드
    # 예: zone_name="AI놀이터" → data/AI놀이터.csv 읽음
```

- `learning.py`의 `_preload_all_zone_csv_rows()`는 **`data/*.csv`만** 로드
- `data/pages/*.csv`는 여기서 사용되지 않음
- 전시물 이미지, 상세 설명, 과학 원리 등이 `data/*.csv`에 있어야 함

---

## 5. 중복 여부 및 데이터 일관성 체크

### 5.1. 완전 중복 (없음)

같은 파일명이 존재해도 내용, 구조, 용도가 모두 다름. **중복된 파일이 없음**.

### 5.2. 데이터 불일치 가능성

| 위험 | 설명 | 예시 |
|---|---|---|
| **전시물명 불일치** | `data/AI놀이터.csv`의 전시물 제목과 `data/pages/AI놀이터.csv`의 섹션 제목이 다를 수 있음 | "지구가 아파요" vs "함께 만드는 우리의 미래" |
| **정보 시점 차이** | `data/*.csv`는 전시물품 대장 (비교적 고정), `data/pages/*.csv`는 크롤링 시점 (변동) | 운영시간 변경 시 pages/는 최신, data/는 구버전 |
| **누락된 전시물** | `data/`에는 있지만 `data/pages/`에는 없는 전시물, 또는 반대 | 신규 전시물 추가 후 크롤링 미반영 |

### 5.3. 데이터 동기화 권장 사항

1. **전시물 변경 시**: `data/*.csv` 먼저 업데이트 → `chroma_db/` 삭제 후 재생성
2. **홈페이지 변경 시**: `scripts/`의 크롤링 스크립트 실행 → `data/pages/` 업데이트 → 벡터 DB 재생성
3. **정기 크롤링**: 공지사항, 운영안내 등은 주기적으로 크롤링하여 `data/pages/` 최신화

---

## 6. 파일별 용도 요약표

### `data/*.csv` — 전시물품 대장 데이터

| 파일명 | 용도 | 사용 위치 |
|---|---|---|
| `AI놀이터.csv` | AI/로봇 관련 전시물 정보 | RAG, learning.py |
| `관찰놀이터.csv` | 관찰/자연 관련 전시물 정보 | RAG, learning.py |
| `생각놀이터.csv` | 사고/논리 관련 전시물 정보 | RAG, learning.py |
| `행동놀이터.csv` | 신체/운동 관련 전시물 정보 | RAG, learning.py |
| `탐구놀이터널.csv` | 탐구/실험 관련 전시물 정보 | RAG, learning.py |
| `천체투영관.csv` | 천체투영관 상영 영상 정보 | RAG, learning.py |
| `공지사항.csv` | 공지사항 요약 | RAG |
| `관람료.csv` | 입장료/무료 대상 정보 | RAG, 규칙기반 |
| `시설안내.csv` | 편의시설 정보 | RAG, 규칙기반 |
| `예약안내.csv` | 예약 방법 안내 | RAG, 규칙기반 |
| `운영안내.csv` | 운영시간/휴관일 | RAG, 규칙기반 |
| `교통안내.csv` | 대중교통/주차 정보 | RAG, 규칙기반 |
| `층별안내.csv` | 층별 전시물 위치 | RAG, 규칙기반 |

### `data/pages/*.csv` — 홈페이지 크롤링 데이터

| 파일명 | 원본 URL | 용도 |
|---|---|---|
| `AI놀이터.csv` | `/centers/exhibitinfo_5.jsp` | AI놀이터 소개 페이지 |
| `관찰놀이터.csv` | `/centers/exhibitinfo_4.jsp` | 관찰놀이터 소개 페이지 |
| `생각놀이터.csv` | `/centers/exhibitinfo_3.jsp` | 생각놀이터 소개 페이지 |
| `행동놀이터.csv` | `/centers/exhibitinfo_2.jsp` | 행동놀이터 소개 페이지 |
| `탐구놀이터.csv` | `/centers/exhibitinfo_1.jsp` | 탐구놀이터 소개 페이지 |
| `천체투영관.csv` | `/centers/exhibitinfo_7.jsp` | 천체투영관 소개 페이지 |
| `공지사항.csv` | `/board/board_1.jsp` | 최신 공지사항 목록 |
| `교통안내.csv` | `/centers/location.jsp` | 오시는 길/교통 정보 |
| `시설안내.csv` | `/centers/facilities.jsp` | 시설(편의시설) 안내 |
| `예약안내.csv` | `/reservation/reservation.jsp` | 예약 방법 안내 |
| `이용안내.csv` | `/visit/guide.jsp` | 관람/이용 안내 |
| `홈페이지.csv` | `/index.jsp` | 메인 페이지 콘텐츠 |
| `개인예약.csv` | `/reservation/reservation_person.jsp` | 개인 예약 페이지 |
| `단체예약.csv` | `/reservation/reservation_group.jsp` | 단체 예약 페이지 |
| `교육예약.csv` | `/reservation/reservation_edu.jsp` | 교육 예약 페이지 |
| `전시해설.csv` | `/program/program_1.jsp` | 전시해설 프로그램 |
| `과학쇼.csv` | `/program/program_2.jsp` | 과학쇼 프로그램 |
| `과학교육실.csv` | `/program/program_3.jsp` | 과학교육실 프로그램 |
| `어린이교실.csv` | `/program/program_4.jsp` | 어린이교실 프로그램 |
| `창작교실1~4.csv` | `/program/program_5~8.jsp` | 창작교실 프로그램 |
| `천체관측소.csv` | `/program/program_9.jsp` | 천체관측소 프로그램 |
| `메타버스과학관.csv` | `/program/program_10.jsp` | 메타버스과학관 |
| `연혁.csv` | `/intro/history.jsp` | 과학관 연혁 |
| `조직도.csv` | `/intro/organization.jsp` | 조직도/부서 안내 |
| `인사말.csv` | `/intro/greeting.jsp` | 관장 인사말 |
| `자주묻는질문.csv` | `/board/faq.jsp` | FAQ 목록 |
| `오시는길.csv` | `/centers/location.jsp` | 오시는 길 (교통안내와 동일 URL) |

---

## 7. 데이터 관리 체크리스트

- [ ] 신규 전시물 추가 시 `data/*.csv`에 반영 후 벡터 DB 재생성
- [ ] 홈페이지 공지/운영시간 변경 시 `scripts/` 크롤링 실행
- [ ] `data/`와 `data/pages/`의 같은 이름 파일이 **내용이 다름**을 기억 (중복 아님)
- [ ] `learning.py`는 `data/*.csv`만 사용, `data/pages/*.csv`는 사용 안 함
- [ ] RAG는 두 폴더를 모두 임베딩하므로, 어느 한쪽만 업데이트하면 정보 불일치 발생

---

> **요약**: `data/`는 **전시물 상세 정보**(전시물품 대장), `data/pages/`는 **홈페이지 콘텐츠**(크롤링). 이름이 같아도 내용과 용도가 다르므로 **중복이 아님**.
