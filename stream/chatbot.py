import os, sys, time
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

import streamlit as st
from init import client,api_key
from stream.sidebar import render_sidebar

ASSISTANT_ID = 'asst_j7j218aEcKkMVWNkXiUH9QVQ'

def chatbot_page(delay = 0.05):
    if "openai_api_key" not in st.session_state:
        st.session_state["openai_api_key"] = api_key


    st.title("💬🤖 Nocoding AI Chatbot with streaming")
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
                    content=prompt
                )
                print(response)

                run = client.beta.threads.runs.create(
                    thread_id= st.session_state["thread_id"],
                    assistant_id=ASSISTANT_ID,
                    stream=True,
                    instructions="""
                   	-	사용자의 언어로 질문에 답변합니다.

                    -	사용자가 다음 요청을 하는 경우 지정된 형식으로 답변합니다:
                        •	문서에서 사용자에게 적합한 모델을 찾아 추천.
                        •	모든 정보는 모델에 대한 충분한 설명이 포함된 문서에서 얻을 수 있음.
                        •	문서 안의 모델은 모두 "NocodingAI" 웹 페이지에서 쉽게 사용할 수 있도록 제공하고 있습니다.

                    -	답변 형식:
                        
                        1.	"(문서에서 선택한 모델의 이름)"
                            •   "(선택 이유 또는 사용자가 이 모델을 사용하기 적합한 이유)"
                                "(필요하다면 추가 지침이나 유용한 정보를 포함. 조언도 환영.)"
                            
                        •	최대 3개의 모델 추천 가능.
                        •	사용자가 요청하는 경우에만 링크 제공.

                    -	주의사항:
                        •	출처를 알려주지 않음.
                        •	400자를 넘지 않도록 답변.
                        •	출처를 제공하지 않음.
                """
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
                            msg += item.text.value
                            place_holder.markdown(msg + "▌")  # 커서 효과 추가
                            time.sleep(delay)  # 각 메시지 전송 후 지연

                elif hasattr(event, "data") and event.data.object == "thread.run.completed":
                    # 완료되면 루프를 중단
                    break

            # 최종 응답에서 커서를 제거하고, 최종 메시지를 화면에 고정하여 출력
            place_holder.markdown(msg)
            st.session_state.messages.append({"role": "assistant", "content": msg})  



