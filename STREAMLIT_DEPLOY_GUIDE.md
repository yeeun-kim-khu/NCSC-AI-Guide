# 🚀 Streamlit Cloud 배포 가이드

## 📋 배포 전 체크리스트

### ✅ 완료된 항목
- [x] 파일 통합 완료 (10개 → 4개)
- [x] 폴더 구조 정리 (data/, multilingual/)
- [x] requirements.txt 준비
- [x] .gitignore 설정
- [x] .streamlit/config.toml 생성

### 🔲 배포 전 필요한 작업
- [ ] GitHub 리포지토리 생성
- [ ] 코드 업로드
- [ ] Streamlit Cloud 계정 생성
- [ ] OpenAI API 키 설정

---

## 📁 현재 프로젝트 구조

```
0406/
├── app_with_voice.py          # 메인 앱 ⭐
├── core.py                    # 핵심 시스템
├── learning.py                # 학습 시스템
├── voice.py                   # 음성 처리
├── requirements.txt           # 패키지 목록 ⭐
├── .gitignore                # Git 설정 ⭐
├── README.md                  # 프로젝트 설명
│
├── .streamlit/               # Streamlit 설정 ⭐
│   ├── config.toml           # 테마 설정
│   └── secrets.toml.template # API 키 템플릿
│
├── data/                     # CSV 데이터 ⭐
│   ├── AI놀이터.csv
│   ├── 관찰놀이터.csv
│   ├── 탐구놀이터.csv
│   └── 행동놀이터.csv
│
└── multilingual/             # 다국어 브로셔 ⭐
    ├── CHN.pdf
    ├── ENG.pdf
    └── JPN.pdf
```

---

## 🔧 1단계: GitHub 리포지토리 준비

### A. GitHub에서 새 리포지토리 생성

1. **GitHub 접속**: https://github.com
2. **New repository** 클릭
3. **설정**:
   - Repository name: `science-museum-guide` (또는 원하는 이름)
   - Description: `국립어린이과학관 AI 가이드`
   - Public (공개) 선택
   - **README 추가 안 함** (이미 있음)
   - **gitignore 추가 안 함** (이미 있음)
4. **Create repository** 클릭

### B. 로컬 Git 설정 및 업로드

프로젝트 폴더에서 Git Bash 또는 터미널 실행:

```bash
# 1. Git 초기화 (이미 되어 있으면 생략)
git init

# 2. 모든 파일 추가
git add .

# 3. 커밋
git commit -m "Initial commit: Consolidated museum guide app"

# 4. GitHub 리포지토리 연결 (YOUR-USERNAME을 본인 계정으로 변경)
git remote add origin https://github.com/YOUR-USERNAME/science-museum-guide.git

# 5. 업로드
git branch -M main
git push -u origin main
```

**⚠️ 주의**: `YOUR-USERNAME`을 본인의 GitHub 사용자명으로 변경하세요!

---

## ☁️ 2단계: Streamlit Cloud 배포

### A. Streamlit Cloud 계정 생성

1. **접속**: https://streamlit.io/cloud
2. **Sign up** 또는 **GitHub로 로그인**
3. GitHub 계정 연동 승인

### B. 앱 배포하기

1. **New app** 클릭
2. **설정**:
   - **Repository**: `YOUR-USERNAME/science-museum-guide` 선택
   - **Branch**: `main`
   - **Main file path**: `app_with_voice.py` ⭐
3. **Advanced settings** 클릭
4. **Python version**: `3.11` 선택 (권장)

### C. Secrets 설정 (중요! ⭐)

**Advanced settings**에서 **Secrets** 섹션에 다음 입력:

```toml
OPENAI_API_KEY = "sk-your-actual-openai-api-key-here"
```

**⚠️ 중요**: 
- 실제 OpenAI API 키를 입력하세요
- 따옴표 포함해서 입력
- 절대 GitHub에 업로드하지 마세요!

5. **Deploy!** 클릭

---

## ⏱️ 3단계: 배포 대기

### 배포 과정 (약 5-10분 소요)

1. **Installing dependencies** (패키지 설치)
   - requirements.txt의 모든 패키지 설치
   - 가장 오래 걸리는 단계

2. **Building app** (앱 빌드)
   - Streamlit 앱 준비

3. **Running** (실행)
   - 앱이 성공적으로 실행되면 URL 생성
   - 예: `https://your-app-name.streamlit.app`

### 배포 로그 확인

- 오른쪽 하단 **Manage app** → **Logs** 확인
- 오류 발생 시 로그에서 원인 확인

---

## 🐛 4단계: 문제 해결

### 자주 발생하는 오류

#### 1. **ModuleNotFoundError**
```
원인: requirements.txt에 패키지가 누락됨
해결: requirements.txt에 해당 패키지 추가 후 재배포
```

#### 2. **OpenAI API 키 오류**
```
원인: Secrets에 API 키가 없거나 잘못됨
해결: Streamlit Cloud → App settings → Secrets에서 확인/수정
```

#### 3. **파일 경로 오류**
```
원인: CSV/PDF 파일 경로가 잘못됨
해결: core.py의 경로가 상대 경로로 되어 있는지 확인
```

#### 4. **메모리 부족**
```
원인: Streamlit Cloud 무료 플랜 제한 (1GB)
해결: 불필요한 데이터 제거 또는 유료 플랜 고려
```

---

## ✅ 5단계: 배포 확인

### 앱이 정상 작동하는지 확인

1. **기본 기능**
   - [ ] 앱이 로드되는가?
   - [ ] 챗봇이 응답하는가?
   - [ ] 음성 입력이 작동하는가?

2. **데이터 로딩**
   - [ ] CSV 데이터가 로드되는가?
   - [ ] RAG 검색이 작동하는가?
   - [ ] 전시물 정보가 표시되는가?

3. **사후 학습**
   - [ ] 퀴즈 생성이 되는가?
   - [ ] 과학동화 생성이 되는가?

---

## 🔄 6단계: 업데이트 방법

코드 수정 후 재배포:

```bash
# 1. 변경사항 커밋
git add .
git commit -m "Update: 설명"

# 2. GitHub에 푸시
git push origin main
```

**자동 재배포**: GitHub에 푸시하면 Streamlit Cloud가 자동으로 재배포합니다!

---

## 📱 7단계: 모바일 최적화 확인

배포된 앱을 모바일에서 테스트:

1. **스마트폰 브라우저**에서 앱 URL 접속
2. **확인 사항**:
   - [ ] 레이아웃이 모바일에 맞게 표시되는가?
   - [ ] 음성 입력이 작동하는가?
   - [ ] 터치 인터페이스가 잘 작동하는가?

---

## 🎉 완료!

축하합니다! 이제 전 세계 어디서나 접속 가능한 AI 과학관 가이드가 완성되었습니다!

### 앱 URL 공유

배포된 앱 URL:
```
https://your-app-name.streamlit.app
```

이 URL을 공유하면 누구나 사용할 수 있습니다!

---

## 📊 무료 플랜 제한사항

Streamlit Cloud 무료 플랜:
- ✅ 공개 앱 무제한
- ✅ 1GB 메모리
- ✅ 1 CPU 코어
- ✅ 자동 재배포
- ⚠️ 비활성 시 자동 슬립 (재접속 시 깨어남)

---

## 🔗 유용한 링크

- **Streamlit Cloud**: https://streamlit.io/cloud
- **Streamlit 문서**: https://docs.streamlit.io
- **배포 가이드**: https://docs.streamlit.io/streamlit-community-cloud/get-started

---

## 💡 팁

1. **앱 이름 변경**: Streamlit Cloud → Settings → General → App name
2. **커스텀 도메인**: 유료 플랜에서 가능
3. **비공개 앱**: Private repository 사용 (GitHub Pro 필요)
4. **성능 모니터링**: Streamlit Cloud → App metrics

---

**준비되셨나요? 위 단계를 따라 배포를 시작하세요!** 🚀
