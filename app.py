import streamlit as st
from stream import sidebar, chatbot, json_answer


if 'current_page' not in st.session_state:
    st.session_state.current_page = 'chatbot' # 기본페이지

sidebar.render_sidebar()

if st.session_state.current_page == 'chatbot':
    chatbot.chatbot_page()
elif st.session_state.current_page == 'json_answer':
    json_answer.chatbot_page()
