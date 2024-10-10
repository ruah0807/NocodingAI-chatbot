import os, sys, time
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from openai import OpenAI
import streamlit as st
from init import client,api_key

ass_id = 'asst_j7j218aEcKkMVWNkXiUH9QVQ'

if "openai_api_key" not in st.session_state:
    st.session_state["openai_api_key"] = api_key

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password", value=api_key )
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    # "[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
    # "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

    client = OpenAI(api_key=openai_api_key)

    thread_id = st.text_input("Thread ID")
    thread_btn = st.button('Create a new thread')

    if thread_btn:
        thread = client.beta.threads.create()
        thread_id = thread.id

        st.subheader(f"{thread_id}", divider="rainbow")
        st.info("스레드가 생성되었습니다.")


st.title("💬🤖 Nocoding AI Chatbot ")
# st.caption("🚀 A Streamlit chatbot powered by OpenAI")
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Please choose language, 'English' or '한국어'"}]

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()
    if not thread_id:
        st.info("Please add your Thread ID to continue.")
        st.stop()

    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    response = client.beta.threads.messages.create(
        thread_id=thread_id,
        role='user',
        content=prompt
    )
    print(response)

    run = client.beta.threads.runs.create(
        thread_id= thread_id,
        assistant_id=ass_id,
    )
    run_id = run.id

    while True:
        run = client.beta.threads.runs.retrieve(
            thread_id=thread_id,
            run_id=run_id
        )
        if run.status == "completed":
            break
        else:
            time.sleep(1)
        print(run.status)

    thread_messages = client.beta.threads.messages.list(thread_id)
    # print(thread_messages.data)

    msg = thread_messages.data[0].content[0].text.value
    print(msg)

    st.session_state.messages.append({"role": "assistant", "content": msg})  
    st.chat_message("assistant").write(msg)

    # response = client.chat.completions.create(model="gpt-4o", messages=st.session_state.messages)
    # msg = response.choices[0].message.content
    # st.session_state.messages.append({"role": "assistant", "content": msg})  
    # st.chat_message("assistant").write(msg)