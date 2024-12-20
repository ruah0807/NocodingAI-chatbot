import os, sys, time, re
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

import streamlit as st
from init import client,api_key
from stream.sidebar import render_sidebar

ASSISTANT_ID = 'asst_j7j218aEcKkMVWNkXiUH9QVQ'

def chatbot_page(delay = 0.05):
    if "openai_api_key" not in st.session_state:
        st.session_state["openai_api_key"] = api_key


    st.title("💬🤖 Nocoding AI Chatbot with json")
    # st.caption("🚀 A Streamlit chatbot powered by OpenAI")

    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Please choose language, 'English' or '한국어' or other languagues"}]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if prompt := st.chat_input():
        if not st.session_state.get("openai_api_key"):
            st.info("Please add your OpenAI API key to continue.")
            st.stop()
        if st.session_state["thread_id"] is None:
            st.info("스레드를 먼저 생성해주세요.")
            st.stop()

        st.session_state.messages.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        # Placeholder 생성 - 한 글자씩 스트리밍할 위치
        place_holder = st.chat_message("assistant")

        with place_holder: 
            with st.spinner("응답을 기다리는 중..."):
            
                response = client.beta.threads.messages.create(
                    thread_id=st.session_state["thread_id"],
                    role='user',
                    content=f"""Question : {prompt} \n\n # Answer Only in JSON Format : \n\n If the question is Korean, answer in Korean. If the question is English, answer in English."""
                )
                print(response)

                run = client.beta.threads.runs.create(
                    thread_id= st.session_state["thread_id"],
                    assistant_id=ASSISTANT_ID,
                    stream=True,
                    temperature=0.76,
                    top_p=0.9,
                    instructions="""
Find the models only in the documents that are provided in the vector database.

You MUST recommend at least one model from the documents, even if it's not a perfect match.
If you can't find an exact match, recommend the closest related models.

Only answer in JSON format.

# Answer JSON Format :    
{{
    "answer" : "(total reason)",
    "models" : [
        {
            "model" : "(model name)", 
            "description" : "(model's description)"
        },
        # ... // If it has more model to recommend.
    ]
}}

Important:
- You MUST include at least 1 model in the response
- Never return an empty models array
- If no exact match is found, recommend the most relevant models from the documents
- Focus on finding ANY models that could potentially help, even if not perfect matches
- If the question is Korean, answer in Korean. If the question is English, answer in English.
""",
                )
                print(run)

                # run_id = run.id
                # 세션 상태에 messages 초기화 (처음 실행 시에만)
                if "messages" not in st.session_state:
                    st.session_state["messages"] = [{"role": "assistant", "content": ""}]

                msg = ""  # 스트리밍 중간 상태를 저장하는 임시 변수
                place_holder = st.empty()  # 한 개의 위치에 메시지를 유지하기 위한 공간
                
            # 스트리밍을 통해 실시간으로 업데이트하고, 완료 시에만 최종 메시지 출력
            for event in run:
                if hasattr(event, "data") and event.data.object == "thread.message.delta":
                    delta_content = event.data.delta.content
                    for item in delta_content:
                        if hasattr(item, "text") and hasattr(item.text, "value"):
                            # 출처 표시 제거
                            text_value = item.text.value
                            print(text_value)
                            text_value = re.sub(r'【.*?】', '', text_value)
                            msg += text_value
                            place_holder.markdown(msg + "▌")  # 커서 효과 추가
                            time.sleep(delay)  # 각 메시지 전송 후 지연

                elif hasattr(event, "data") and event.data.object == "thread.run.completed":
                    # 완료되면 루프를 중단
                    break

            # 최종 응답에서 커서를 제거하고, 최종 메시지를 화면에 고정하여 출력
            place_holder.markdown(msg)
            st.session_state.messages.append({"role": "assistant", "content": msg})  



