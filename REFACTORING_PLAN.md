# 파일 통합 리팩토링 계획

## 현재 문제점
- 파일이 너무 세분화되어 있어 관리가 어려움
- 관련 기능들이 여러 파일에 분산되어 있음
- import 관계가 복잡함

## 통합 계획

### 방안 1: 기능별 통합 (권장)

```
📁 프로젝트 구조
├── app.py                      # 메인 앱 (app_with_voice.py 이름 변경)
├── config.py                   # 설정 및 상수 (constants.py + rules.py 통합)
├── core/
│   ├── __init__.py
│   ├── rag_system.py          # RAG 시스템 (rag.py + multilingual_loader.py)
│   └── tools.py               # LangChain 도구 (tools.py 유지)
├── features/
│   ├── __init__.py
│   ├── voice.py               # 음성 처리 (voice_handler.py)
│   ├── learning.py            # 사후 학습 (post_visit_learning.py + audiobook_generator.py)
│   └── visualization.py       # 시각화 (visualization.py 유지)
├── utils.py                   # 유틸리티 (utils.py 유지)
└── requirements.txt
```

**통합 내용:**
1. **config.py** ← constants.py + rules.py
2. **core/rag_system.py** ← rag.py + multilingual_loader.py
3. **features/learning.py** ← post_visit_learning.py + audiobook_generator.py
4. **features/voice.py** ← voice_handler.py
5. **app.py** ← app_with_voice.py (이름만 변경)

**장점:**
- 파일 수: 15개 → 9개
- 관련 기능이 한 곳에 모임
- import 경로가 명확해짐
- 확장성 좋음

---

### 방안 2: 최소 통합 (보수적)

```
📁 프로젝트 구조
├── app.py                      # 메인 앱
├── config.py                   # 설정 (constants.py + rules.py)
├── rag.py                      # RAG (rag.py + multilingual_loader.py)
├── tools.py                    # LangChain 도구
├── learning.py                 # 학습 (post_visit_learning.py + audiobook_generator.py)
├── voice.py                    # 음성 (voice_handler.py)
├── utils.py                    # 유틸리티
├── visualization.py            # 시각화
└── requirements.txt
```

**통합 내용:**
1. **config.py** ← constants.py + rules.py
2. **rag.py** ← rag.py + multilingual_loader.py
3. **learning.py** ← post_visit_learning.py + audiobook_generator.py
4. **voice.py** ← voice_handler.py
5. **app.py** ← app_with_voice.py

**장점:**
- 파일 수: 15개 → 9개
- 간단한 구조
- 기존 import 경로 변경 최소화

---

### 방안 3: 단일 파일 (극단적)

```
📁 프로젝트 구조
├── museum_guide_app.py         # 모든 기능 통합 (5000+ 줄)
├── requirements.txt
└── data/
    ├── *.csv
    └── *.pdf
```

**통합 내용:**
- 모든 Python 파일을 하나로 통합

**단점:**
- 파일이 너무 커짐 (5000+ 줄)
- 유지보수 어려움
- **권장하지 않음**

---

## 권장 사항: 방안 2 (최소 통합)

### 통합 상세 계획

#### 1. config.py (constants.py + rules.py)
```python
# config.py - 모든 설정과 규칙을 한 곳에

# 전시관 정보
STATIC_EXHIBIT_INFO = {...}
CSC_URLS = {...}

# 규칙
GUARDRAILS = {...}
REASONING_STEPS = {...}
```

#### 2. rag.py (rag.py + multilingual_loader.py)
```python
# rag.py - RAG 시스템 전체

def load_csv_data(): ...
def load_multilingual_brochures(): ...
def initialize_vector_db(): ...
```

#### 3. learning.py (post_visit_learning.py + audiobook_generator.py)
```python
# learning.py - 사후 학습 전체 기능

# 퀴즈 & 질문
def generate_quiz(): ...
def interactive_learning_chat(): ...

# 오디오북
def generate_science_story(): ...
def text_to_audiobook(): ...

# UI
def render_post_visit_learning(): ...
```

#### 4. voice.py (voice_handler.py)
```python
# voice.py - 음성 입출력

def speech_to_text(): ...
def text_to_speech(): ...
def get_language_code(): ...
def autoplay_audio(): ...
```

---

## 실행 순서

1. ✅ 새 파일 생성 및 코드 통합
2. ✅ import 경로 수정
3. ✅ 테스트 실행
4. ✅ 구 파일 삭제

---

## 예상 효과

- **파일 수**: 15개 → 9개 (40% 감소)
- **코드 관리**: 관련 기능이 한 곳에 모여 이해하기 쉬움
- **import 간소화**: 
  - Before: `from constants import X; from rules import Y`
  - After: `from config import X, Y`
- **확장성**: 새 기능 추가 시 어디에 넣을지 명확함

---

## 주의사항

- 기존 파일은 백업 후 삭제
- import 경로 변경으로 인한 오류 확인 필요
- 단계적으로 진행 (한 번에 하나씩)
