import os, sys, time
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from openai import OpenAI
import streamlit as st
from init import client,api_key

ass_id = 'asst_j7j218aEcKkMVWNkXiUH9QVQ'

if "openai_api_key" not in st.session_state:
    st.session_state["openai_api_key"] = api_key

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", 
                                   key="chatbot_api_key", 
                                   type="password", 
                                   value=api_key )

    client = OpenAI(api_key=openai_api_key)

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



st.title("💬🤖 Nocoding AI Chatbot ")
# st.caption("🚀 A Streamlit chatbot powered by OpenAI")

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Please choose language, 'English' or '한국어' or other languagues"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()
    if st.session_state["thread_id"] is None:
        st.info("스레드를 먼저 생성해주세요.")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    place_holder = st.chat_message("assistant")
    with place_holder: 
        with st.spinner("응답을 기다리는 중..."):
        
            response = client.beta.threads.messages.create(
                thread_id=st.session_state["thread_id"],
                role='user',
                content=prompt
            )
            # print(response)

            run = client.beta.threads.runs.create(
                thread_id= st.session_state["thread_id"],
                assistant_id=ass_id,
            )
            run_id = run.id

            while True:
                run = client.beta.threads.runs.retrieve(
                    thread_id=st.session_state["thread_id"],
                    run_id=run_id
                )
                if run.status == "completed":
                    break
                else:
                    time.sleep(2)
                print(run.status)

            thread_messages = client.beta.threads.messages.list(st.session_state["thread_id"])
            # print(thread_messages.data)

            msg = thread_messages.data[0].content[0].text.value
            print(msg)

            # 로딩메세지를 실제 응답으로 교체
            place_holder.write(msg)
            st.session_state.messages.append({"role": "assistant", "content": msg})  


