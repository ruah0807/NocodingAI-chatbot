import streamlit as st
from stream import sidebar, chatbot, other_page


if 'current_page' not in st.session_state:
    st.session_state.current_page = 'chatbot' # 기본페이지

sidebar.render_sidebar()

if st.session_state.current_page == 'chatbot':
    chatbot.chatbot_page()
elif st.session_state.current_page == 'other':
    other_page.other_feature_page()
