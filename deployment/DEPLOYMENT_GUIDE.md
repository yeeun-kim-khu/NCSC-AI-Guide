# 🚀 Streamlit Cloud 배포 완벽 가이드

## ✅ 준비 완료 체크리스트

배포 폴더(`deployment/`)에 다음 파일들이 준비되어 있습니다:

### 필수 파일
- ✅ `app.py` - 메인 애플리케이션
- ✅ `requirements.txt` - Python 패키지 목록
- ✅ `.streamlit/config.toml` - Streamlit 설정
- ✅ `.gitignore` - Git 제외 파일 목록
- ✅ `README.md` - 프로젝트 설명

### 코드 파일
- ✅ `config.py`, `voice.py`, `rag.py`, `tools.py`, `utils.py`
- ✅ `post_visit_learning.py`, `audiobook_generator.py`
- ✅ `multilingual_loader.py`, `visualization.py`

### 데이터 파일
- ✅ CSV 파일 4개 (전시물 데이터)
- ✅ PDF 파일 3개 (다국어 브로셔)

---

## 📋 배포 단계별 가이드

### 1단계: GitHub 리포지토리 생성

#### Option A: 새 리포지토리 생성
1. https://github.com/new 접속
2. Repository name: `csc-ai-guide` (또는 원하는 이름)
3. Public 선택 (Streamlit Cloud 무료 배포는 Public만 가능)
4. "Create repository" 클릭

#### Option B: 기존 리포지토리 사용
- 기존 리포지토리에 `deployment` 폴더를 푸시

---

### 2단계: 코드 업로드

```bash
# deployment 폴더로 이동
cd C:\Users\yeeun\Documents\Space Research\code\2026\0406\deployment

# Git 초기화 (새 리포지토리인 경우)
git init

# 모든 파일 추가
git add .

# 커밋
git commit -m "Initial deployment: CSC AI Guide"

# GitHub 리포지토리 연결 (본인의 URL로 변경)
git remote add origin https://github.com/YOUR-USERNAME/csc-ai-guide.git

# 푸시
git branch -M main
git push -u origin main
```

**⚠️ 중요:** `.streamlit/secrets.toml` 파일은 `.gitignore`에 포함되어 있어 자동으로 제외됩니다.

---

### 3단계: Streamlit Cloud 배포

#### 3-1. Streamlit Cloud 접속
1. https://share.streamlit.io 접속
2. **"Sign up with GitHub"** 또는 **"Continue with GitHub"** 클릭
3. GitHub 계정으로 로그인

#### 3-2. 새 앱 생성
1. **"New app"** 버튼 클릭
2. 다음 정보 입력:
   - **Repository:** `YOUR-USERNAME/csc-ai-guide`
   - **Branch:** `main`
   - **Main file path:** `app.py`

#### 3-3. Secrets 설정 (중요!)
1. **"Advanced settings"** 클릭
2. **"Secrets"** 섹션에 다음 내용 입력:

```toml
OPENAI_API_KEY = "sk-proj-여기에-실제-API-키-입력"
```

**OpenAI API 키 발급 방법:**
- https://platform.openai.com/api-keys 접속
- "Create new secret key" 클릭
- 생성된 키 복사 (한 번만 표시됨!)

#### 3-4. 배포 시작
1. **"Deploy!"** 버튼 클릭
2. 배포 진행 상황 확인 (약 5-10분 소요)
3. 배포 완료 시 URL 생성: `https://YOUR-APP-NAME.streamlit.app`

---

### 4단계: 배포 확인

#### 4-1. 웹 브라우저에서 확인
생성된 URL을 브라우저에서 열기

#### 4-2. 모바일에서 확인
1. 모바일 브라우저에서 동일한 URL 접속
2. 음성 기능 테스트 (마이크 권한 허용 필요)

#### 4-3. 기능 테스트
- ✅ 챗봇 질문/답변
- ✅ 음성 입력/출력
- ✅ 사후 학습 탭
- ✅ 오디오북 생성

---

## 🔧 배포 후 관리

### 코드 업데이트
```bash
# 코드 수정 후
git add .
git commit -m "Update: 설명"
git push

# Streamlit Cloud가 자동으로 재배포 (약 2-3분)
```

### Secrets 수정
1. Streamlit Cloud 대시보드 접속
2. 앱 선택 → "Settings" → "Secrets"
3. 내용 수정 후 저장
4. 앱 자동 재시작

### 로그 확인
1. Streamlit Cloud 대시보드
2. 앱 선택 → "Manage app" → "Logs"
3. 실시간 로그 및 오류 확인

---

## ⚠️ 주의사항

### 1. API 키 보안
- ❌ **절대** `.streamlit/secrets.toml` 파일을 GitHub에 업로드하지 마세요
- ✅ Streamlit Cloud 웹 UI에서만 Secrets 설정
- ✅ `.gitignore`에 `secrets.toml` 포함 확인

### 2. 비용 관리
**OpenAI API 사용량:**
- GPT-4o: $5/1M input tokens, $15/1M output tokens
- GPT-4o-mini: $0.15/1M input tokens, $0.60/1M output tokens
- Whisper: $0.006/분
- TTS: $15/1M characters

**예상 비용 (월 1000명 사용 기준):**
- 챗봇: 약 $10-20
- 음성 기능: 약 $5-10
- 오디오북: 약 $10-15
- **총 예상: $25-45/월**

**비용 절감 팁:**
- GPT-4o 대신 GPT-4o-mini 사용
- 음성 출력 선택적 활성화
- 사용량 모니터링: https://platform.openai.com/usage

### 3. 성능 최적화
- 첫 방문자는 RAG DB 생성으로 로딩 시간 길 수 있음 (약 30초)
- 이후 방문자는 캐시로 빠른 로딩
- Streamlit Cloud 무료 플랜: 1GB RAM, 1 CPU

---

## 🐛 문제 해결

### 배포 실패
**증상:** 배포 중 오류 발생

**해결:**
1. Streamlit Cloud 로그 확인
2. `requirements.txt` 패키지 버전 확인
3. Python 버전 호환성 (3.9-3.11 권장)

### 음성 기능 작동 안 함
**증상:** 마이크 버튼 클릭 안 됨

**해결:**
1. HTTPS 환경 확인 (Streamlit Cloud는 자동 HTTPS)
2. 브라우저 마이크 권한 허용
3. Chrome/Safari 최신 버전 사용

### RAG 검색 결과 없음
**증상:** "전시물 정보를 찾을 수 없습니다"

**해결:**
1. CSV 파일이 GitHub에 업로드되었는지 확인
2. Streamlit Cloud에서 앱 재시작
3. 로그에서 CSV 로딩 메시지 확인

### API 키 오류
**증상:** "OpenAI API key not found"

**해결:**
1. Streamlit Cloud Secrets 설정 확인
2. API 키 형식 확인 (`sk-proj-...`)
3. OpenAI 계정 크레딧 잔액 확인

---

## 📱 모바일 최적화 팁

### 권장 브라우저
- ✅ Chrome (Android/iOS)
- ✅ Safari (iOS)
- ⚠️ Samsung Internet (음성 기능 제한적)

### 사용자 경험
- 터치 친화적 UI
- 음성 입력으로 편리한 질문
- 오디오북 다운로드 후 오프라인 청취

---

## 🎉 배포 완료!

배포가 성공적으로 완료되면:

1. **URL 공유:** `https://your-app.streamlit.app`
2. **QR 코드 생성:** 과학관 안내판에 부착
3. **모바일 테스트:** 다양한 기기에서 확인
4. **피드백 수집:** 사용자 의견 반영

---

## 📞 추가 지원

### Streamlit 공식 문서
- https://docs.streamlit.io/streamlit-community-cloud

### OpenAI API 문서
- https://platform.openai.com/docs

### 문제 발생 시
- GitHub Issues 활용
- Streamlit Community Forum: https://discuss.streamlit.io
