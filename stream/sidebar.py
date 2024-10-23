import os, sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from openai import OpenAI
import streamlit as st
from init import api_key



def render_sidebar():

    with st.sidebar:
        st.sidebar.header("Navigation")
        if st.sidebar.button("chatbot"):
            st.session_state.current_page = "chatbot"
        if st.sidebar.button("other"):
            st.session_state.current_page = "other"

        st.sidebar.write("---")


        # 페이지 선택 옵션 추가
        openai_api_key = st.text_input("OpenAI API Key", 
                                    key="chatbot_api_key", 
                                    type="password", 
                                    value=api_key )

        client = OpenAI(api_key=openai_api_key)
        
        if "openai_api_key" not in st.session_state:
            st.session_state["openai_api_key"] = api_key

        # thread_id = st.text_input("Thread ID")

        if "thread_id" not in st.session_state:
            st.session_state["thread_id"] = None


        #스레드 생성버튼(스레드가 없을 때만 활성화)
        thread_btn = st.button('스레드 생성하기')
        if thread_btn:
            if st.session_state["thread_id"] is None:
                thread = client.beta.threads.create()
                st.session_state["thread_id"] = thread.id
                st.info("스레드가 생성되었습니다. 대화를 시작할 수 있습니다.")
                # st.subheader(f"{thread_id}", divider="rainbow")
            else:   
                st.warning("스레드가 이미 존재합니다. 삭제 후 재생성 해주세요 ")


        thread_del_btn = st.button("스레드 삭제")
        if thread_del_btn:
            if st.session_state["thread_id"] is not None:
                thread_del = client.beta.threads.delete(st.session_state["thread_id"])
                st.session_state["thread_id" ]= None
                st.info(f"스레드가 삭제되었습니다. 대화를 시작하시려면 새로운 스래드를 생성해주세요.")
            else: 
                st.warning("삭제할 스래드가 존재하지 않습니다.")


