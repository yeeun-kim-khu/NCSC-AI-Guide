# post_visit_learning.py - 사후 학습 시스템
import streamlit as st
from langchain_openai import ChatOpenAI
from rag import initialize_vector_db
import random

# 놀이터 기본 정보 (층수와 설명만)
ZONE_INFO = {
    "AI놀이터": {
        "floor": "1층",
        "description": "AI와 로봇 기술의 원리를 배워요",
        "has_data": True
    },
    "생각놀이터": {
        "floor": "1층",
        "description": "생각하는 힘을 키워요",
        "has_data": False  # CSV 없음
    },
    "행동놀이터": {
        "floor": "1층",
        "description": "몸을 움직이며 과학을 배워요",
        "has_data": True
    },
    "천체투영관": {
        "floor": "1층",
        "description": "우주와 별의 비밀을 알아봐요",
        "has_data": False  # CSV 없음
    },
    "탐구놀이터": {
        "floor": "2층",
        "description": "생활 속 과학원리를 탐구해요",
        "has_data": True
    },
    "관찰놀이터": {
        "floor": "2층",
        "description": "자연을 관찰하며 배워요",
        "has_data": True
    },
    "빛놀이터": {
        "floor": "2층",
        "description": "빛의 신비를 체험해요",
        "has_data": False  # CSV 없음
    }
}

def get_zone_exhibits_from_rag(zone_name, vector_db):
    """RAG에서 해당 놀이터의 전시물 정보 가져오기"""
    try:
        # 방법 1: 메타데이터 필터링으로 검색
        try:
            docs = vector_db.similarity_search(
                zone_name,
                k=50,
                filter={"category": zone_name}
            )
        except:
            # 필터링이 안되면 일반 검색
            docs = vector_db.similarity_search(zone_name, k=50)
        
        exhibits = []
        seen_titles = set()  # 중복 제거
        
        for doc in docs:
            # 메타데이터의 category 확인
            category = doc.metadata.get("category", "")
            title = doc.metadata.get("title", "")
            content = doc.page_content
            
            # 디버깅: 첫 5개 문서의 category 출력
            if len(exhibits) < 5:
                print(f"DEBUG - Category: '{category}', Zone: '{zone_name}', Match: {zone_name in category}")
            
            # 놀이터 이름이 정확히 일치하는 문서만 필터링
            if zone_name in category and title not in seen_titles:
                exhibits.append({
                    "content": content,
                    "metadata": doc.metadata
                })
                seen_titles.add(title)
        
        print(f"최종 검색 결과: {zone_name}에서 {len(exhibits)}개 전시물 발견")
        return exhibits
    except Exception as e:
        print(f"RAG 검색 오류: {e}")
        import traceback
        traceback.print_exc()
        return []

def extract_principles_from_exhibits(exhibits, llm):
    """전시물에서 과학원리 추출 - 원리 목록과 설명 반환"""
    if not exhibits:
        return [], ""
    
    # 전시물 정보를 텍스트로 결합
    exhibit_text = "\n\n".join([ex["content"] for ex in exhibits[:10]])  # 상위 10개
    
    prompt = f"""다음 전시물들에서 핵심 과학원리를 추출해주세요.

전시물 정보:
{exhibit_text}

**응답 형식:**
1. 먼저 과학원리 목록을 쉼표로 구분하여 한 줄로 작성하세요.
   예: 빛의 굴절, 소리의 진동, 전기회로, 자기장, 에너지 변환

2. 그 다음 각 원리에 대한 설명을 작성하세요.
   - 원리명: 간단한 설명 (1-2문장)

최대 5-7개의 핵심 원리를 추출하세요."""

    try:
        response = llm.invoke(prompt)
        content = response.content
        
        # 첫 번째 줄에서 원리 목록 추출
        lines = content.strip().split('\n')
        principles_line = lines[0] if lines else ""
        
        # 쉼표로 구분된 원리들 추출
        principles = [p.strip() for p in principles_line.split(',') if p.strip()]
        
        # 숫자나 특수문자로 시작하는 경우 제거
        principles = [p.split('.')[-1].strip() if '.' in p else p for p in principles]
        
        return principles, content
    except Exception as e:
        print(f"원리 추출 오류: {e}")
        return [], "원리를 추출할 수 없습니다."

def generate_quiz(zone_name, principle, llm, language="한국어"):
    """과학원리 기반 퀴즈 생성"""
    
    language_prompts = {
        "한국어": f"""'{zone_name}'의 '{principle}' 원리에 대한 퀴즈를 만들어주세요.

퀴즈 형식:
**질문**: [어린이가 이해하기 쉬운 질문]

**선택지**:
1. [정답]
2. [오답1]
3. [오답2]
4. [오답3]

**정답**: 1번

**해설**: [정답인 이유를 쉽게 설명]

어린이 눈높이에 맞춰 재미있고 교육적인 퀴즈를 만들어주세요!""",
        
        "English": f"""Create a quiz about the '{principle}' principle from '{zone_name}'.

Quiz format:
**Question**: [Easy-to-understand question for children]

**Choices**:
1. [Correct answer]
2. [Wrong answer 1]
3. [Wrong answer 2]
4. [Wrong answer 3]

**Answer**: 1

**Explanation**: [Explain why this is correct in simple terms]

Make it fun and educational for children!""",
        
        "日本語": f"""'{zone_name}'の'{principle}'の原理についてのクイズを作ってください。

クイズ形式:
**質問**: [子供が理解しやすい質問]

**選択肢**:
1. [正解]
2. [不正解1]
3. [不正解2]
4. [不正解3]

**答え**: 1番

**解説**: [正解の理由を簡単に説明]

子供向けに楽しく教育的なクイズを作ってください！""",
        
        "中文": f"""为'{zone_name}'的'{principle}'原理创建一个测验。

测验格式:
**问题**: [儿童易于理解的问题]

**选项**:
1. [正确答案]
2. [错误答案1]
3. [错误答案2]
4. [错误答案3]

**答案**: 1

**解释**: [用简单的语言解释为什么这是正确的]

请创建一个有趣且有教育意义的儿童测验！"""
    }
    
    prompt = language_prompts.get(language, language_prompts["한국어"])
    
    try:
        response = llm.invoke(prompt)
        return response.content
    except Exception as e:
        print(f"퀴즈 생성 오류: {e}")
        return "퀴즈를 생성할 수 없습니다."

def interactive_learning_chat(zone_name, principle, llm, user_question, language="한국어"):
    """과학원리에 대한 대화형 학습"""
    
    language_prompts = {
        "한국어": f"""당신은 '{zone_name}'의 '{principle}' 원리를 가르치는 친절한 과학 선생님입니다.

어린이의 질문: {user_question}

어린이 눈높이에 맞춰 쉽고 재미있게 설명해주세요. 
- 이모지 사용 ✨🔬🌟
- 쉬운 비유와 예시
- 짧고 명확한 문장
- 격려와 칭찬""",
        
        "English": f"""You are a friendly science teacher explaining the '{principle}' principle from '{zone_name}'.

Child's question: {user_question}

Explain in a fun and easy way for children:
- Use emojis ✨🔬🌟
- Simple analogies and examples
- Short, clear sentences
- Encouragement and praise""",
        
        "日本語": f"""あなたは'{zone_name}'の'{principle}'の原理を教える優しい科学の先生です。

子供の質問: {user_question}

子供の目線に合わせて楽しく簡単に説明してください:
- 絵文字を使う ✨🔬🌟
- 簡単な例えと例
- 短くて明確な文
- 励ましと褒め言葉""",
        
        "中文": f"""你是一位友好的科学老师，正在解释'{zone_name}'的'{principle}'原理。

孩子的问题: {user_question}

用有趣且简单的方式为孩子们解释:
- 使用表情符号 ✨🔬🌟
- 简单的类比和例子
- 简短明了的句子
- 鼓励和赞扬"""
    }
    
    prompt = language_prompts.get(language, language_prompts["한국어"])
    
    try:
        response = llm.invoke(prompt)
        return response.content
    except Exception as e:
        print(f"대화 생성 오류: {e}")
        return "답변을 생성할 수 없습니다."

def render_post_visit_learning(vector_db, language_mode="한국어"):
    """사후 학습 시스템 UI"""
    
    st.title("🎓 오늘 배운 과학원리 복습하기")
    
    # 학습 모드 탭
    learning_tab1, learning_tab2 = st.tabs(["📚 퀴즈 & 질문", "🎧 나만의 과학동화"])
    
    language_text = {
        "한국어": {
            "subtitle": "과학관에서 체험한 놀이터를 선택하고, 그 안에 숨겨진 과학원리를 배워봐요!",
            "floor1": "1층 전시관",
            "floor2": "2층 전시관",
            "select_prompt": "오늘 방문한 놀이터를 선택해주세요 (여러 개 선택 가능)",
            "start_learning": "학습 시작하기! 🚀",
            "no_selection": "놀이터를 먼저 선택해주세요!",
            "learning_zone": "학습 중인 놀이터",
            "principles": "핵심 과학원리",
            "quiz_mode": "퀴즈 모드",
            "chat_mode": "질문하기 모드",
            "generate_quiz": "퀴즈 풀기 🎯",
            "ask_question": "궁금한 점 물어보기 💬"
        },
        "English": {
            "subtitle": "Select the zones you visited and learn the science principles hidden inside!",
            "floor1": "1st Floor Exhibitions",
            "floor2": "2nd Floor Exhibitions",
            "select_prompt": "Select the zones you visited today (multiple selections allowed)",
            "start_learning": "Start Learning! 🚀",
            "no_selection": "Please select a zone first!",
            "learning_zone": "Learning Zone",
            "principles": "Key Scientific Principles",
            "quiz_mode": "Quiz Mode",
            "chat_mode": "Q&A Mode",
            "generate_quiz": "Take Quiz 🎯",
            "ask_question": "Ask Questions 💬"
        },
        "日本語": {
            "subtitle": "訪れたゾーンを選んで、その中に隠された科学の原理を学びましょう！",
            "floor1": "1階展示館",
            "floor2": "2階展示館",
            "select_prompt": "今日訪れたゾーンを選んでください（複数選択可）",
            "start_learning": "学習開始！ 🚀",
            "no_selection": "まずゾーンを選んでください！",
            "learning_zone": "学習中のゾーン",
            "principles": "主要な科学原理",
            "quiz_mode": "クイズモード",
            "chat_mode": "質問モード",
            "generate_quiz": "クイズに挑戦 🎯",
            "ask_question": "質問する 💬"
        },
        "中文": {
            "subtitle": "选择您参观过的区域，学习其中隐藏的科学原理！",
            "floor1": "1楼展览馆",
            "floor2": "2楼展览馆",
            "select_prompt": "选择您今天参观的区域（可多选）",
            "start_learning": "开始学习！ 🚀",
            "no_selection": "请先选择一个区域！",
            "learning_zone": "学习区域",
            "principles": "核心科学原理",
            "quiz_mode": "测验模式",
            "chat_mode": "问答模式",
            "generate_quiz": "参加测验 🎯",
            "ask_question": "提问 💬"
        }
    }
    
    text = language_text.get(language_mode, language_text["한국어"])
    
    # 놀이터 선택 UI (탭 밖에서 정의)
    st.markdown(f"### {text['subtitle']}")
    
    # 1층 놀이터
    st.markdown(f"#### 🏢 {text['floor1']}")
    floor1_zones = ["AI놀이터", "생각놀이터", "행동놀이터", "천체투영관"]
    
    cols1 = st.columns(4)
    selected_zones = []
    
    for idx, zone in enumerate(floor1_zones):
        with cols1[idx]:
            zone_info = ZONE_INFO[zone]
            if zone_info['has_data']:
                if st.checkbox(f"{zone}\n{zone_info['description']}", key=f"zone_{zone}"):
                    selected_zones.append(zone)
            else:
                st.checkbox(f"{zone}\n{zone_info['description']}\n(준비 중)", key=f"zone_{zone}", disabled=True)
    
    # 2층 놀이터
    st.markdown(f"#### 🏢 {text['floor2']}")
    floor2_zones = ["탐구놀이터", "관찰놀이터", "빛놀이터"]
    
    cols2 = st.columns(3)
    
    for idx, zone in enumerate(floor2_zones):
        with cols2[idx]:
            zone_info = ZONE_INFO[zone]
            if zone_info['has_data']:
                if st.checkbox(f"{zone}\n{zone_info['description']}", key=f"zone_{zone}"):
                    selected_zones.append(zone)
            else:
                st.checkbox(f"{zone}\n{zone_info['description']}\n(준비 중)", key=f"zone_{zone}", disabled=True)
    
    st.markdown("---")
    
    if selected_zones:
        st.success(f"✅ {text['select_prompt']}: {', '.join(selected_zones)}")
        
        # 학습 모드 선택
        learning_mode = st.radio(
            "학습 방식 선택:",
            ["퀴즈 풀기 🎯", "자유 질문 💬"],
            horizontal=True
        )
        
        # 놀이터별 학습
        for zone in selected_zones:
            with st.expander(f"📚 {zone} - {ZONE_INFO[zone]['description']}", expanded=True):
                
                # RAG에서 전시물 정보 가져오기
                exhibits = get_zone_exhibits_from_rag(zone, vector_db)
                
                if exhibits:
                    st.info(f"📊 {zone}에서 {len(exhibits)}개의 전시물 정보를 찾았습니다!")
                    
                    st.markdown(f"**🔬 {text['principles']}:**")
                    
                    # LLM으로 과학원리 추출
                    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
                    zone_principles, principles_text = extract_principles_from_exhibits(exhibits, llm)
                    st.markdown(principles_text)
                    
                    st.markdown("---")
                    
                    if zone_principles:  # 원리가 추출된 경우에만
                        if learning_mode == "퀴즈 풀기 🎯":
                            # 퀴즈 모드
                            st.markdown(f"### {text['quiz_mode']}")
                            
                            # 동적으로 추출된 원리 선택
                            selected_principle = st.selectbox(
                                "학습할 원리 선택:",
                                zone_principles,
                                key=f"principle_{zone}"
                            )
                            
                            if st.button(f"{text['generate_quiz']}", key=f"quiz_{zone}"):
                                with st.spinner("퀴즈 생성 중..."):
                                    quiz = generate_quiz(zone, selected_principle, llm, language_mode)
                                    st.markdown(quiz)
                        
                        else:
                            # 질문하기 모드
                            st.markdown(f"### {text['chat_mode']}")
                            
                            # 동적으로 추출된 원리 선택
                            selected_principle = st.selectbox(
                                "궁금한 원리 선택:",
                                zone_principles,
                                key=f"principle_chat_{zone}"
                            )
                            
                            user_question = st.text_input(
                                f"{text['ask_question']}:",
                                placeholder="예: 빛은 왜 굽어요?",
                                key=f"question_{zone}"
                            )
                        
                        if user_question:
                            with st.spinner("답변 생성 중..."):
                                answer = interactive_learning_chat(
                                    zone, selected_principle, llm, user_question, language_mode
                                )
                                st.markdown(f"**🤖 답변:**\n\n{answer}")
                else:
                    st.warning(f"{zone}의 전시물 정보를 찾을 수 없습니다.")
        
        else:
            st.info(f"ℹ️ {text['no_selection']}")
    
    with learning_tab2:
        # 오디오북 생성 기능
        from audiobook_generator import render_audiobook_generator
        render_audiobook_generator(selected_zones, vector_db, language_mode)
