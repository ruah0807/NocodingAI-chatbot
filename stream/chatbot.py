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
                    - Answer the question with user's language.
                    - Only answer questions related to NocodingAI. Do not respond to other inquiries.
                        - Thins related to 'NocodingAI' :
                            - making their own website.
                            - using AI model only from document
                            - recommend the models.
                            - having side job with AI.
                            - solo developer
                            - AI models from documents
                            - greeting

                    - If the user makes the following requests, respond in the specified format:
                        - Find and suggest a suitable model for the user from the documents.
                        - All information can be obtained from the documents containing sufficient descriptions of the models.
                    - Answer Format:
                        - Include any overall instructions or helpful information if necessary. Offering advice is also appreciated.
                        1.	(Mode's name from document)
                          -	(Reason for selection or why this model is suitable for the user)
                        
                        - You can recommend up to 3 models.
                        - provide the links if the user requests them, Each model has a link in the documents.
                    - If the user asks a question unrelated to NocodingAI:
	                    - Please respond in the same language as the user's input:
                            ex) “I can only answer questions related to NocodingAI. What would you like to create with generative AI? I can recommend suitable models.”
                    - Don't let them know the sources where you found.
                    - Do not answer more than 400 characters.
                    - Do not give the sources.
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



