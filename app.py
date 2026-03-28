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

# FAISS 벡터 DB는 앱 실행 시 한 번만 로드되도록 캐싱
@st.cache_resource
def load_rag_db():
    return initialize_vector_db()

def main():
    st.set_page_config(page_title="국립어린이과학관 AI 가이드", page_icon="🐣", layout="centered")

    if "OPENAI_API_KEY" not in os.environ:
        os.environ["OPENAI_API_KEY"] = st.secrets.get("OPENAI_API_KEY", "")

    # RAG 시스템 로드
    vector_db = load_rag_db()

    with st.sidebar:
        st.title("⚙️ 안내 모드")
        user_mode = st.radio(["어린이", "청소년/성인"], index=1)
        if st.button("대화 새로고침 🔄"):
            st.session_state.messages = []
            st.session_state.thread_id = uuid.uuid4().hex
            st.session_state.debug_logs = []
            st.rerun()

    st.title("국립어린이과학관 AI 가이드🤖")

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