# 🐣 국립어린이과학관 AI 가이드

국립어린이과학관 방문객을 위한 AI 기반 음성 가이드 시스템

## 🌟 주요 기능

### 1. 🤖 AI 챗봇 가이드
- 과학관 운영 정보, 전시관 안내, 예약 방법 등 실시간 질문 응답
- 어린이/청소년/성인 모드별 맞춤 답변
- 다국어 지원 (한국어, English, 日本語, 中文)

### 2. 🎤 음성 입출력
- 음성으로 질문하고 음성으로 답변 듣기
- OpenAI Whisper (음성인식) + TTS (음성합성)
- 모바일 친화적 인터페이스

### 3. 🎓 사후 학습 시스템
- 방문한 전시관별 과학원리 퀴즈
- 인터랙티브 Q&A 학습
- 개인 맞춤형 복습 콘텐츠

### 4. 🎧 나만의 과학동화
- 체험한 전시물 기반 과학동화 자동 생성
- 오디오북으로 변환하여 다운로드
- 잠들기 전 복습용 콘텐츠

## 🚀 Streamlit Cloud 배포 가이드

### 1단계: GitHub 리포지토리 준비

```bash
# deployment 폴더로 이동
cd deployment

# Git 초기화 (새 리포지토리인 경우)
git init

# 파일 추가
git add .

# 커밋
git commit -m "Initial deployment setup"

# GitHub 리포지토리 연결
git remote add origin https://github.com/your-username/your-repo.git

# 푸시
git push -u origin main
```

### 2단계: Streamlit Cloud 배포

1. **https://share.streamlit.io** 접속
2. **GitHub 계정으로 로그인**
3. **"New app" 클릭**
4. **리포지토리 설정:**
   - Repository: `your-username/your-repo`
   - Branch: `main`
   - Main file path: `app.py`
5. **"Advanced settings" 클릭**
6. **Secrets 설정:**
   ```toml
   OPENAI_API_KEY = "sk-your-actual-api-key-here"
   ```
7. **"Deploy!" 클릭**

### 3단계: 배포 완료

배포가 완료되면 다음과 같은 URL이 생성됩니다:
```
https://your-app-name.streamlit.app
```

이 URL을 모바일 브라우저에서 열면 바로 사용 가능합니다!

## 📱 모바일 최적화

- 반응형 디자인으로 모바일에서도 사용 가능
- 음성 녹음 기능은 HTTPS 환경에서만 작동 (Streamlit Cloud는 자동 HTTPS)
- 터치 친화적 UI

## 🔧 기술 스택

- **Frontend:** Streamlit
- **LLM:** OpenAI GPT-4o, GPT-4o-mini
- **RAG:** LangChain + Chroma Vector DB
- **Voice:** OpenAI Whisper (STT) + TTS
- **Data:** CSV 전시물 데이터 + PDF 다국어 브로셔

## 📂 프로젝트 구조

```
deployment/
├── app.py                          # 메인 앱
├── config.py                       # 설정 + 규칙
├── voice.py                        # 음성 처리
├── rag.py                          # RAG 시스템
├── tools.py                        # LangChain 도구
├── utils.py                        # 유틸리티
├── post_visit_learning.py          # 사후 학습
├── audiobook_generator.py          # 오디오북 생성
├── multilingual_loader.py          # 다국어 로더
├── visualization.py                # 시각화
├── requirements.txt                # Python 패키지
├── .streamlit/
│   ├── config.toml                # Streamlit 설정
│   └── secrets.toml               # API 키 (로컬용)
├── *.csv                          # 전시물 데이터
├── *.pdf                          # 다국어 브로셔
└── README.md                      # 이 파일
```

## ⚠️ 주의사항

### API 키 보안
- `.streamlit/secrets.toml` 파일은 **절대 GitHub에 업로드하지 마세요**
- Streamlit Cloud 웹 UI에서 직접 Secrets 설정
- `.gitignore`에 `secrets.toml`이 포함되어 있는지 확인

### 비용 관리
- OpenAI API 사용량에 따라 비용 발생
- GPT-4o는 GPT-4o-mini보다 비용이 높음
- 음성 기능 (Whisper + TTS)도 사용량에 따라 과금

### 성능 최적화
- Chroma DB는 첫 실행 시 자동 생성 (약 30초 소요)
- `@st.cache_resource`로 RAG DB 캐싱
- 배포 후 첫 방문자는 로딩 시간이 길 수 있음

## 🐛 문제 해결

### 배포 실패 시
1. `requirements.txt` 패키지 버전 확인
2. Python 버전 호환성 확인 (3.9-3.11 권장)
3. Streamlit Cloud 로그 확인

### 음성 기능 작동 안 함
1. HTTPS 환경인지 확인 (Streamlit Cloud는 자동 HTTPS)
2. 브라우저 마이크 권한 허용
3. 모바일에서는 브라우저별로 지원 여부 다름

### RAG 검색 결과 없음
1. CSV 파일이 올바르게 업로드되었는지 확인
2. Chroma DB 재생성 (캐시 삭제 후 재배포)

## 📞 문의

프로젝트 관련 문의사항이 있으시면 GitHub Issues를 이용해주세요.

## 📄 라이선스

이 프로젝트는 국립어린이과학관 방문객 경험 향상을 위해 개발되었습니다.
