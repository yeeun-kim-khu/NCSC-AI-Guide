# app.py
import os
import uuid
import streamlit as st
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver

from tools import get_tools
from rules import route_intent, answer_rule_based
from utils import get_dynamic_prompt, render_source_buttons
from rag import initialize_vector_db

# Optimized RAG loading with progress indication
@st.cache_resource
def load_rag_db():
    """Load RAG database with caching"""
    with st.spinner("RAG database loading..."):
        from rag import initialize_vector_db
        vector_db = initialize_vector_db()
        st.success("RAG database ready!")
    return vector_db

def main():
    st.set_page_config(page_title="국립어린이과학관 AI 가이드", page_icon="🐣", layout="centered")

    if "OPENAI_API_KEY" not in os.environ:
        os.environ["OPENAI_API_KEY"] = st.secrets.get("OPENAI_API_KEY", "")

    # RAG 시스템 로드
    vector_db = load_rag_db()

    with st.sidebar:
        st.title("⚙️ 안내 모드")
        user_mode = st.selectbox("사용자 모드 선택:", options=["어린이", "청소년/성인"], index=1)
        
        # Language mode selection
        language_mode = st.selectbox(
            "언어 모드 선택:",
            options=["한국어", "English", "日本語", "中文"],
            format_func=lambda x: {
                "한국어": "한국어",
                "English": "English", 
                "日本語": "日本語",
                "中文": "中文"
            }[x],
            index=0
        )
        
        if st.button("대화 새로고침 🔄"):
            st.session_state.messages = []
            st.session_state.thread_id = uuid.uuid4().hex
            st.session_state.debug_logs = []
            st.rerun()

    st.title("국립어린이과학관 AI 가이드🤖")
    
    # Architecture Overview Section
    with st.expander("LLM-based Active Scientific Principle Exploration Architecture", expanded=False):
        st.markdown("Architecture visualization temporarily disabled due to graphviz dependency.")
        st.markdown("Key components working: LLM Agent, RAG System, Real-time Tools")

    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "thread_id" not in st.session_state:
        st.session_state.thread_id = uuid.uuid4().hex
    if "debug_logs" not in st.session_state:
        st.session_state.debug_logs = []

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)
    memory = MemorySaver()
    agent = create_react_agent(
        model=llm,
        tools=get_tools(),
        prompt=get_dynamic_prompt(user_mode),
        checkpointer=memory,
    )

    for i, msg in enumerate(st.session_state.messages):
        if msg["role"] == "debug":
            with st.expander("🔍 디버깅 정보(도구 호출 내역)"):
                with st.container(height=400):
                    st.text(msg["content"])
        else:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    user_input = st.chat_input("질문을 입력해주세요!")
    
    # Recommended Questions
    if not st.session_state.messages:
        st.markdown("### 💡 추천 질문")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🔬 과학 원리", key="science"):
                user_input = "빛이 굽는 원리가 궁금해요!"
        with col2:
            if st.button("🏛️ 전시관 안내", key="exhibit"):
                user_input = "탐구놀이터에서 뭐 할 수 있어요?"
        with col3:
            if st.button("📅 운영 정보", key="info"):
                user_input = "내일 가도 돼요?"
    
    # Process Flow Visualization
    if st.session_state.messages and any(msg.get("role") == "debug" for msg in st.session_state.messages[-3:]):
        # with st.expander("🔄 현재 처리 과정", expanded=False):
        #     render_process_flow()
        pass
    
    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        intent = route_intent(user_input)
        
        with st.chat_message("assistant"):
            if intent in ["notice", "basic"]:
                # 규칙 기반 엔진 동작 (RAG/LLM 미사용, 속도 최적화)
                with st.spinner("(규칙기반)확인 중입니다..."):
                    answer = answer_rule_based(intent, user_input, user_mode)
                st.markdown(answer)
                render_source_buttons(answer)
            else:
                # LLM + RAG + Crawling 엔진 동작
                with st.spinner("(LLM)잠시만 기다려 주세요..."):
                    # FAISS RAG에서 관련 정보 사전 검색하여 컨텍스트 주입
                    retrieved_docs = vector_db.similarity_search(user_input, k=3)
                    rag_context = "\n\n".join([f"[{doc.metadata.get('source', 'N/A')}]\n{doc.page_content}" for doc in retrieved_docs])
                    
                    # RAG 컨텍스트를 시스템 메시지로 추가 (사용자 메시지와 분리)
                    config = {"configurable": {"thread_id": st.session_state.thread_id}}
                    messages = [
                        {"role": "system", "content": f"[RAG 배경지식]\n{rag_context}"},
                        {"role": "user", "content": user_input}
                    ]
                    result = agent.invoke({"messages": messages}, config=config)
                    answer = result["messages"][-1].content
                    
                    # 디버깅 로그 수집 (RAG 검색 결과 포함)
                    debug_info = f"=== RAG 검색 결과 (k=3) ===\n{rag_context}\n\n{'='*50}\n\n"
                    for msg in result["messages"][:-1]:  # 마지막 답변 제외
                        if hasattr(msg, 'pretty_repr'):
                            debug_info += msg.pretty_repr() + "\n\n"
                        elif hasattr(msg, 'content'):
                            debug_info += str(msg.content) + "\n\n"
                    
                st.markdown(answer)
                render_source_buttons(answer)
                
                # 디버깅 정보 표시 (답변 뒤)
                if debug_info.strip():
                    with st.expander("🔍 디버깅 정보 (도구 호출 내역)"):
                        with st.container(height=400):
                            st.text(debug_info)
                    st.session_state.messages.append({"role": "debug", "content": debug_info})

        st.session_state.messages.append({"role": "assistant", "content": answer})

if __name__ == "__main__":
    main()