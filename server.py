import os
import csv
import streamlit as st
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

@st.cache_data
def load_products():
    with open('EYES_analysis_final_cleaned.csv', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)

products = load_products()

st.title("메이크업 챗봇 - 보우나")

if 'messages' not in st.session_state:
    st.session_state['messages'] = [
        {"role": "assistant", "content": "안녕하세요, 보우나입니다. 더 예쁘고 나답게 빛나기 위한 여정을 시작해볼까요?"}
    ]

for msg in st.session_state['messages']:
    st.chat_message("assistant" if msg['role'] == 'assistant' else "user").write(msg['content'])

user_input = st.chat_input("메시지를 입력하세요")
if user_input:
    st.session_state['messages'].append({"role": "user", "content": user_input})
    with st.spinner("답변 생성 중..."):
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=st.session_state['messages']
        )
        reply = response.choices[0].message.content
    st.session_state['messages'].append({"role": "assistant", "content": reply})
    st.chat_message("user").write(user_input)
    st.chat_message("assistant").write(reply)

st.subheader("E.Y.E.S 코드로 제품 검색")
eyes_code = st.text_input("코드를 입력하세요")
if st.button("추천 보기") and eyes_code:
    code = eyes_code.upper()
    recs = [p for p in products if code in p['eyes_code'].upper()][:5]
    for i, p in enumerate(recs, 1):
        st.write(f"{i}. {p['product_name']} - {p['description']} (가격: {p['price']})")
