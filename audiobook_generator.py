# audiobook_generator.py - 과학동화 오디오북 생성
import streamlit as st
from langchain_openai import ChatOpenAI
from openai import OpenAI
import os

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def generate_science_story(zone_name, exhibits, principles, language="한국어"):
    """방문한 놀이터 기반 과학동화 생성"""
    
    # 전시물 정보 요약
    exhibit_summary = "\n".join([f"- {ex['metadata'].get('title', '')}" for ex in exhibits[:5]])
    principles_text = ", ".join(principles[:3])
    
    language_prompts = {
        "한국어": f"""당신은 어린이를 위한 과학동화 작가입니다.

**배경:**
오늘 어린이가 '{zone_name}'에서 다음 전시물들을 체험했습니다:
{exhibit_summary}

이 전시물들에는 다음과 같은 과학원리가 담겨 있습니다:
{principles_text}

**요청:**
이 체험을 바탕으로 5-7분 분량의 과학동화를 만들어주세요.

**동화 구성:**
1. 주인공: 호기심 많은 어린이 (이름: 지우)
2. 스토리: 지우가 '{zone_name}'에서 체험한 내용을 모험 이야기로 구성
3. 과학원리: 자연스럽게 녹여서 설명
4. 톤: 따뜻하고 재미있게, 잠들기 전 듣기 좋은 분위기
5. 길이: 약 1000-1500자

**중요:**
- 어린이가 이해하기 쉬운 단어 사용
- 과학원리를 억지로 설명하지 말고 이야기 속에 자연스럽게 녹이기
- 긍정적이고 희망찬 결말
- 잠들기 전 듣기 좋은 차분한 분위기""",

        "English": f"""You are a children's science storyteller.

**Background:**
Today, a child visited '{zone_name}' and experienced these exhibits:
{exhibit_summary}

These exhibits contain the following scientific principles:
{principles_text}

**Request:**
Create a 5-7 minute science bedtime story based on this experience.

**Story Structure:**
1. Protagonist: A curious child (Name: Jiwoo)
2. Story: Turn Jiwoo's experience at '{zone_name}' into an adventure
3. Science: Naturally weave in the scientific principles
4. Tone: Warm, fun, perfect for bedtime
5. Length: About 1000-1500 characters

**Important:**
- Use simple, child-friendly language
- Don't force science explanations - make them natural
- Positive, hopeful ending
- Calm atmosphere suitable for bedtime listening"""
    }
    
    prompt = language_prompts.get(language, language_prompts["한국어"])
    
    try:
        llm = ChatOpenAI(model="gpt-4o", temperature=0.8)  # 창의성을 위해 temperature 높임
        response = llm.invoke(prompt)
        return response.content
    except Exception as e:
        print(f"동화 생성 오류: {e}")
        return None

def text_to_audiobook(story_text, language="한국어"):
    """텍스트를 오디오북으로 변환 (OpenAI TTS)"""
    
    # 언어별 음성 선택
    voice_map = {
        "한국어": "nova",    # 부드럽고 따뜻한 여성 목소리
        "English": "alloy",  # 중성적이고 차분한 목소리
        "日本語": "shimmer", # 밝고 친근한 목소리
        "中文": "fable"      # 서정적인 목소리
    }
    
    voice = voice_map.get(language, "nova")
    
    try:
        # OpenAI TTS API 호출
        response = client.audio.speech.create(
            model="tts-1-hd",  # 고품질 음성
            voice=voice,
            input=story_text,
            speed=0.9  # 잠들기 전 듣기 좋게 약간 느리게
        )
        
        return response.content
    except Exception as e:
        print(f"오디오북 생성 오류: {e}")
        return None

def render_audiobook_generator(selected_zones, vector_db, language_mode="한국어"):
    """오디오북 생성 UI"""
    
    st.markdown("### 🎧 나만의 과학동화 만들기")
    st.info("💡 오늘 체험한 놀이터를 바탕으로 잠들기 전 들을 수 있는 과학동화를 만들어드려요!")
    
    if not selected_zones:
        st.warning("먼저 체험한 놀이터를 선택해주세요!")
        return
    
    # 놀이터 선택 확인
    st.markdown(f"**선택한 놀이터:** {', '.join(selected_zones)}")
    
    if st.button("🎨 나만의 과학동화 만들기", type="primary"):
        
        # 각 놀이터의 전시물과 원리 수집
        from post_visit_learning import get_zone_exhibits_from_rag, extract_principles_from_exhibits
        
        all_exhibits = []
        all_principles = []
        
        for zone in selected_zones:
            exhibits = get_zone_exhibits_from_rag(zone, vector_db)
            if exhibits:
                all_exhibits.extend(exhibits)
                
                llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.7)
                principles, _ = extract_principles_from_exhibits(exhibits, llm)
                all_principles.extend(principles)
        
        if not all_exhibits:
            st.error("전시물 정보를 찾을 수 없습니다.")
            return
        
        # 동화 생성
        with st.spinner("✨ 당신만을 위한 과학동화를 만들고 있어요... (30초 소요)"):
            story = generate_science_story(
                ", ".join(selected_zones),
                all_exhibits,
                all_principles,
                language_mode
            )
        
        if story:
            st.success("✅ 과학동화가 완성되었어요!")
            
            # 동화 텍스트 표시
            with st.expander("📖 동화 내용 보기", expanded=True):
                st.markdown(story)
            
            # 오디오북 생성
            with st.spinner("🎙️ 오디오북으로 변환 중... (1분 소요)"):
                audio_bytes = text_to_audiobook(story, language_mode)
            
            if audio_bytes:
                st.success("🎧 오디오북이 완성되었어요!")
                
                # 오디오 플레이어
                st.audio(audio_bytes, format="audio/mp3")
                
                # 다운로드 버튼
                st.download_button(
                    label="💾 오디오북 다운로드",
                    data=audio_bytes,
                    file_name=f"과학동화_{selected_zones[0]}.mp3",
                    mime="audio/mp3"
                )
                
                st.info("💤 잠들기 전에 들으면서 오늘 배운 과학원리를 복습해보세요!")
            else:
                st.error("오디오북 생성에 실패했습니다.")
        else:
            st.error("동화 생성에 실패했습니다.")
