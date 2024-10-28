import os, sys, time
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import streamlit as st
from init import client,api_key
from stream.sidebar import render_sidebar

ASSISTANT_ID = 'asst_j7j218aEcKkMVWNkXiUH9QVQ'


def chatbot_page():
    if "openai_api_key" not in st.session_state:
        st.session_state["openai_api_key"] = api_key


    st.title("💬🤖 Nocoding AI Chatbot ")
    # st.caption("🚀 A Streamlit chatbot powered by OpenAI")

    if "messages" not in st.session_state:
        st.session_state["messages"] = [{"role": "assistant", "content": "Please choose language, 'English' or '한국어' or other languagues"}]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input():
        if not render_sidebar.openai_api_key:
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
                print(response)

                run = client.beta.threads.runs.create(
                    thread_id= st.session_state["thread_id"],
                    assistant_id=ASSISTANT_ID,
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


