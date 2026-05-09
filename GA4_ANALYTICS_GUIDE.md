# GA4 (Google Analytics 4) 분석 설정 및 이벤트 추적 가이드

> **측정 ID**: `G-7VS14G0T7P`  
> **적용 대상**: `app_with_voice.py` (로컬/클라우드), `learning.py` (로컬/클라우드)  
> **수집 원칙**: 개인정보(PII) 및 대화 내용(질문/답변 텍스트) 수집 금지

---

## 1. GA4 웹스트림 설정 방법

### 1.1. Google Analytics 4 속성 생성

1. [Google Analytics](https://analytics.google.com) 접속
2. **관리(톱니바퀴 아이콘) → 속성 생성**
3. 속성 이름: `국립어린이과학관-AI-가이드` (자유)
4. 보고 시간대: `한국 표준시`
5. 통화: `KRW`
6. **업종 카테고리**: `교육 > 박물관/과학관` 또는 `기술 > 컴퓨터 및 전자제품`
7. **비즈니스 규모**: 소규모 (방문자 수 기준)

### 1.2. 웹 데이터 스트림 추가

1. **관리 → 데이터 수집 및 수정 → 데이터 스트림 → 웹**
2. 스트림 URL:
   - 배포 주소 입력 (예: `https://ncsc-ai-guide.streamlit.app`)
   - 또는 `localhost` 테스트용으로 `http://localhost:8501` 입력 (테스트 후 삭제 권장)
3. 스트림 이름: `NCSC-AI-Guide-Streamlit`
4. **측정 ID 확인**: 생성 후 `G-7VS14G0T7P` 형식의 ID가 표시됨
5. **이 ID를 코드의 `_init_google_analytics()` 함수에 반영**

### 1.3. 개인정보 보호 설정 (필수)

GA4 속성에서 다음 설정을 반드시 적용:

| 설정 경로                            | 설정 값                     | 이유                      |
| ------------------------------------ | --------------------------- | ------------------------- |
| **관리 → 데이터 설정 → 데이터 수집** | `IP 주소 익명화` ON         | GDPR/개인정보보호법 준수  |
| **관리 → 데이터 설정 → Google 신호** | `광고 개인정보보호` OFF     | 광고 타겟팅 방지          |
| **관리 → 데이터 설정 → 데이터 보관** | `14개월` 또는 `26개월`      | 과도한 보관 방지          |
| **관리 → 계정 설정 → 계정 세부정보** | `데이터 공유 설정` 모두 OFF | Google에 데이터 판매 방지 |

코드에서도 이미 다음 프라이버시 설정이 주입됨:

```javascript
gtag("config", "G-XXXXXXX", {
  anonymize_ip: true,
  allow_google_signals: false,
  allow_ad_personalization_signals: false,
  restricted_data_processing: true,
  send_page_view: true,
  cookie_flags: "SameSite=None;Secure",
});
```

### 1.4. 맞춤 이벤트 등록 (선택이나 권장)

GA4 콘솔에서 보고서 필터링을 쉽게 하려면 맞춤 이벤트를 등록:

1. **관리 → 데이터 표시 → 맞춤 정의 → 맞춤 이벤트 만들기**
2. 이벤트 이름 입력 (아래 표 참조)
3. 조건 없이 그대로 등록 (모든 매개변수 자동 수집)

등록 권장 이벤트:

- `send_message`
- `answer_delivered`
- `answer_feedback`
- `faq_button_click`
- `quick_menu_click`
- `voice_input_used`
- `tts_played`
- `chat_reset`
- `program_detail_click`
- `quiz_generated`
- `question_asked`
- `story_generated`
- `audiobook_converted`

---

## 2. 수집되는 이벤트 목록

### 2.1. 가이드 탭 (app_with_voice.py)

| 이벤트 이름            | 발생 시점                 | 수집 파라미터                                                           | 분석 용도                              |
| ---------------------- | ------------------------- | ----------------------------------------------------------------------- | -------------------------------------- |
| `page_view`            | 페이지 접속 시 (GA4 기본) | `page_location`, `page_title`                                           | 방문자 수, 신규/재방문                 |
| `privacy_consent`      | 개인정보 동의 "확인" 클릭 | `language`                                                              | 동의율, 언어별 거부 패턴               |
| `send_message`         | 사용자 질문 전송          | `intent`, `language`, `user_mode`                                       | 의도 분포, 언어별 사용 패턴            |
| `answer_delivered`     | AI 답변 생성 완료         | `intent`, `answer_type`, `language`, `user_mode`                        | 규칙기반 vs LLM 비율, 응답량           |
| `answer_feedback`      | 👍 또는 👎 클릭           | `feedback`(positive/negative), `intent`, `answer_type`, `language`      | **답변 품질 측정**                     |
| `faq_button_click`     | 사이드바 FAQ 버튼 클릭    | `category`(floor/programs/route/exhibits), `language`                   | 어떤 FAQ가 인기 많은지                 |
| `quick_menu_click`     | 메인 빠른메뉴 버튼 클릭   | `category`, `language`                                                  | 버튼 안내 vs 자유입력 선호도           |
| `voice_input_used`     | 음성 입력 성공            | `language`                                                              | 음성 기능 활용률 (어린이 친화성)       |
| `tts_played`           | "음성 듣기" 버튼 클릭     | `language`                                                              | TTS(음성출력) 활용률                   |
| `chat_reset`           | "대화 새로고침" 클릭      | `language`, `user_mode`                                                 | 사용자가 대화를 끝내고 재시작하는 빈도 |
| `program_detail_click` | 프로그램 세부 버튼 클릭   | `category`(explanation/science_show/planetarium/light_zone), `language` | 어떤 프로그램 정보가 궁금한지          |

### 2.2. 또만나 놀이터 탭 (learning.py)

| 이벤트 이름           | 발생 시점                | 수집 파라미터            | 분석 용도                 |
| --------------------- | ------------------------ | ------------------------ | ------------------------- |
| `quiz_generated`      | "퀴즈 만들기" 클릭       | `zone`, `language`       | 퀴즈 기능 활용률          |
| `question_asked`      | "질문하기" 클릭          | `zone`, `language`       | 질문 모드 활용률          |
| `story_generated`     | "과학동화 만들기" 클릭   | `zone_count`, `language` | 동화 생성 기능 활용률     |
| `audiobook_converted` | "오디오북으로 변환" 클릭 | `language`               | 오디오북 변환 기능 활용률 |

### 2.3. 수집되지 않는 데이터 (원칙)

| 항목                                   | 이유                                              |
| -------------------------------------- | ------------------------------------------------- |
| 사용자가 타이핑한 **실제 질문 텍스트** | 개인정보 보호, 추론 가능성 차단                   |
| AI가 생성한 **실제 답변 텍스트**       | 개인정보 포함 가능성, 벡터 DB 원문 노출 우려      |
| `user_id`, `email`, `name` 등 식별자   | 익명화 원칙                                       |
| `thread_id`, `session_id`              | 세션 추적 가능성 (단, GA4 내부 session_id는 사용) |

---

## 3. GA4 보고서에서 확인하는 방법

### 3.1. 실시간 보고서 (즉시 확인)

1. **보고서 → 참여도 → 실시간**
2. 현재 접속 중인 사용자 수 확인
3. **이벤트 카드**에서 방금 발생한 이벤트 목록 확인
4. **지연**: 이벤트 발생 후 5~10분 이내 반영

### 3.2. 이벤트 보고서 (집계 확인)

1. **보고서 → 참여도 → 이벤트**
2. 원하는 이벤트 클릭 → **매개변수** 탭 선택
3. `language`, `user_mode`, `intent`, `answer_type` 등 파라미터별 집계 확인

### 3.3. 탐색분석 (맞춤 차트)

1. **탐색 → 탐색분석 시작 → 자유형**
2. **차원**: `이벤트 이름`, `맞춤 이벤트: language`, `맞춤 이벤트: intent`
3. **지표**: `이벤트 수`, `고유 사용자 수`
4. **필터**: `이벤트 이름` 정확히 일치 `answer_feedback`

이 조합으로 다음 분석이 가능:

- "어느 언어 사용자가 가장 많이 퀴즈를 생성했는가?"
- "규칙기반 답변과 LLM 답변 중 어떤게 👍를 더 많이 받았는가?"
- "FAQ 중 '층별 안내'가 '전시관 안내'보다 몇 배 더 클릭되었는가?"

### 3.4. 경로 탐색 (사용자 여정)

1. **탐색 → 경로 탐색**
2. **시작 이벤트**: `privacy_consent`
3. **다음 단계**: `faq_button_click` → `send_message` → `answer_delivered` → `answer_feedback`
4. 이 경로로 "동의 → FAQ 클릭 → 질문 → 답변 → 피드백" 전체 흐름 시각화 가능

---

## 4. 시범 적용 결과보고에 포함할 핵심 지표

### 4.1. 서비스 활용률 (Adoption)

| 지표                 | GA4 확인 경로                             | 의미                              |
| -------------------- | ----------------------------------------- | --------------------------------- |
| 총 방문자 수 (UV)    | 보고서 → 수명주기 → 획득 → 사용자 수      | 서비스 도달 범위                  |
| 총 질문 수           | 이벤트 → `send_message` 이벤트 수         | 실제 사용 빈도                    |
| 세션당 평균 질문 수  | 탐색분석: 세션당 `send_message` 평균      | 사용자가 얼마나 대화를 이어가는가 |
| 재방문률             | 보고서 → 수명주기 → 획득 → 신규 vs 재방문 | 만족도의 대리지표                 |
| 음성 입력 사용률     | `voice_input_used` / `send_message` × 100 | 어린이 친화성 지표                |
| TTS(음성듣기) 사용률 | `tts_played` / `answer_delivered` × 100   | 접근성/편의성 지표                |

### 4.2. 기능별 선호도 (Feature Usage)

| 지표                                  | 의사결정 예시                             |
| ------------------------------------- | ----------------------------------------- |
| FAQ 버튼 vs 빠른메뉴 vs 자유입력 비율 | 버튼 안내를 선호하면 UI 간소화 가능       |
| FAQ 카테고리별 클릭 순위              | 가장 수요 많은 정보 → 메인 화면 배너 추가 |
| 또만나 놀이터 진입률                  | 사후 학습 기능 인기도                     |
| 퀴즈/동화/오디오북 생성 수            | 교육적 기능 활용도                        |

### 4.3. 언어/사용자층 분석 (Equity)

| 지표                    | 의사결정 예시                                                    |
| ----------------------- | ---------------------------------------------------------------- |
| 언어별 사용 비율        | 외국인 방문객 비율 추정, 다국어 개선 우선순위                    |
| 언어 × 의도 교차 분석   | "영어 사용자가 운영시간을 많이 물어봄" → 외국어 안내 부족        |
| 언어 × answer_type 교차 | "일본어 사용자의 LLM 답변 부정 비율 높음" → 일본어 프롬프트 개선 |

### 4.4. 답변 품질 (Quality)

| 지표                            | 의사결정 예시                           |
| ------------------------------- | --------------------------------------- |
| 규칙기반 답변 만족도 (👍/👎)    | FAQ/안내 콘텐츠의 정확성 검증           |
| LLM+RAG 답변 만족도             | AI 응답 신뢰성 검증                     |
| 의도별 부정 비율                | 어떤 질문 유형에서 답변이 자주 틀리는가 |
| 대화 중단률 (질문 후 세션 종료) | 답변 실망 → 이탈 여부 추정              |

### 4.5. 운영 개선을 위한 핵심 질문

결과보고서에 다음 질문과 데이터를 포함하면 의미 있음:

1. **"가장 많이 묻는 질문 TOP3는 무엇인가?"**
   - → `send_message`의 `intent` 파라미터 집계
2. **"어떤 답변 방식이 더 정확한가?"**
   - → `answer_feedback` × `answer_type` 교차 분석
3. **"어느 언어 사용자가 가장 어려움을 겪는가?"**
   - → 언어별 `answer_feedback=negative` 비율
4. **"사용자가 가장 많이 클릭하는 FAQ는?"**
   - → `faq_button_click`의 `category` 파라미터 집계
5. **"음성 기능이 실제로 쓰이는가?"**
   - → `voice_input_used` / 총 세션 수
6. **"또만나 놀이터(사후 학습) 기능이 활용되는가?"**
   - → `quiz_generated` + `story_generated` 합계

---

## 5. 문제 해결 FAQ

### Q. 이벤트가 GA4에 도착하지 않는다?

1. **Streamlit Cloud에서 iframe 문제**: Streamlit은 iframe 내에서 실행되므로 GA4 스크립트 주입이 필요. 코드의 `_init_google_analytics()`가 `st.markdown(..., unsafe_allow_html=True)`로 주입하는지 확인.
2. **AdBlocker**: 사용자 브라우저의 광고 차단기가 GA4 차단 가능. 테스트 시 시크릿 모드에서 확인.
3. **측정 ID 오류**: `_init_google_analytics()` 함수 내 `G-7VS14G0T7P`가 실제 GA4 속성과 일치하는지 확인.
4. **이벤트 큐 문제**: `_flush_ga_events()`가 `main()` 시작 부분에서 호출되는지 확인.

### Q. `st.rerun()` 직후 이벤트가 사라진다?

- `_queue_ga_event()` 사용. 버튼 클릭 시 큐에 넣고, 다음 렌더링에서 `_flush_ga_events()`로 한 번에 전송.
- 이미 코드에 모두 적용됨.

### Q. 테스트 환경에서 GA4에 쌓이는 데이터를 구분하고 싶다?

- GA4에서 필터 생성: **관리 → 데이터 필터 → 내부 트래픽 필터**
- localhost/내부 IP 필터링하여 테스트 데이터 제외
- 또는 `_track_ga_event`에 `environment: "production"` 파라미터 추가 후 GA4에서 필터링

### Q. 어린이 사용자 데이터 수집에 법적 문제는 없는가?

- **질문/답변 텍스트 수집 안 함** → 개인정보 해당 없음
- **IP 익명화 ON** → 개인 식별 불가
- **광고/마케팅 목적 없음** → 동의 절차 단순화 가능
- 단, **14세 미만 어린이** 대상 서비스일 경우: 개인정보처리방침에 수집 항목 명시 권장

---

## 6. 참고 자료

- [GDPR-Compliant Chatbot Guide (2026)](https://quickchat.ai/post/gdpr-compliant-chatbot-guide)
- [ChatbotKit Ratings Best Practices](https://chatbotkit.com/docs/ratings)
- [IBM WatsonX Feedback Tutorial](https://developer.ibm.com/tutorials/awb-watsonx-assistant-thumbs-up-down-feedback/)
- [Google Analytics 4 이벤트 문서](https://support.google.com/analytics/answer/9322688?hl=ko)
