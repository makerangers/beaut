import streamlit as st
from dotenv import load_dotenv
import os
load_dotenv()
BOUNA_IMAGE_PATH = os.getenv('BOUNA_IMAGE_PATH')

class ChatUI:
    def __init__(self):
        self._init_state("chat_history", [])
        self._show_welcome_once()

    def _init_state(self, key, default):
        if key not in st.session_state:
            st.session_state[key] = default

    def _show_welcome_once(self):
        if not st.session_state.chat_history:
            welcome_msg = self.welcome_message
            st.chat_message("assistant", avatar=BOUNA_IMAGE_PATH).write(welcome_msg)

    @property
    def welcome_message(self):
        return (
        "✨ 저는 뷰티 챗봇 **보우나**예요!\n\n"
        "당신만의 스타일을 찾아 떠나는 여정, 지금 바로 함께 시작해봐요 💖"
        "준비되셨나요?✨"

        )
         #   "**제가 성함을 어떻게 불러드리면 좋을까요? 💗**"
    def render_chat_history(self):
        for msg in st.session_state.chat_history:
            if msg["role"] == "system":
                continue
            avatar = BOUNA_IMAGE_PATH if msg["role"] == "assistant" else None
            st.chat_message(msg["role"], avatar=avatar).write(msg["content"])
