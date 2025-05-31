from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.prompts import ChatPromptTemplate
from system_prompt import BOUNA_SYSTEM_PROMPT
import streamlit as st
import openai
from deep_translator import GoogleTranslator
from dotenv import load_dotenv
import os

load_dotenv()
BOUNA_IMAGE_PATH = os.getenv('BOUNA_IMAGE_PATH')
llm = ChatOpenAI(model='gpt-4o-mini', temperature=0)
memory = ConversationBufferMemory(return_messages=True)

def translate_to_english(prompt):
    # source='auto'는 입력 언어를 자동 감지
    print(f"Translating prompt to English: {prompt}")  # 디버깅용 출력
    translated = GoogleTranslator(source='auto', target='en').translate(prompt)
    return translated

def handle(query):
    if "system_prompt_sent" not in st.session_state:
        st.session_state.system_prompt_sent = False
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    if not st.session_state.system_prompt_sent:
        st.session_state.chat_history.append({
            "role": "system",
            "content": BOUNA_SYSTEM_PROMPT
        })
        st.session_state.system_prompt_sent = True

    st.chat_message("user").write(query)
    st.session_state.chat_history.append({
        "role": "user",
        "content": query
    })

    prompt = PromptTemplate(
        input_variables=["history", "input"],
        template=BOUNA_SYSTEM_PROMPT + "\n\n{history}\n\n사용자: {input}\n보우나:")


    chain = ConversationChain(
        llm=llm,
        memory=memory,
        prompt=prompt,
        verbose=True
    )

    result = chain.predict(input=query)

    st.chat_message("assistant", avatar=BOUNA_IMAGE_PATH).write(result)
    st.session_state.chat_history.append({
        "role": "assistant",
        "content": result
    })
    

def eyes_report(symbol):
    prompt = """
            E.Y.E.S 코드 중 {symbol} 가 무엇을 의미하는지, 각 알파벳이 어떤 기준을 나타내는지,누구나 쉽게 이해할 수 있도록 친근하게 한국어로 설명해줘. 구체적인 제품이나 예시 없이 코드의 체계와 자리별 의미만 부드럽게 안내해줘.
        """
    prompt = ChatPromptTemplate.from_messages([
        ("system", BOUNA_SYSTEM_PROMPT),
        ("user", prompt)
    ])

    output_parser = StrOutputParser()
    chain = prompt | llm | output_parser

    result = chain.invoke({
        "symbol": symbol
    })
    
    return result

# 이미지 프롬프트 자동 생성 함수
def generate_eyes_image(effect_type):
    image_prompt = (
        "눈을 클로우즈업하여 메이크업한 실사 이미지를 생성해 눈의 디테일이 강조되고, 자연스러운 조명과 색감을 사용하여 눈의 아름다움을 극대화해줘.")
    english_prompt =  translate_to_english(image_prompt)
    english_prompt = "With a dreamlike soft close-up, her beautiful eyes and flawless skin stand out. Her eyes are softly lined with pencil eyeliner to complete a natural and elegant makeup look. The image is in a sketch style in a fashion magazine."
    print(f"Translated prompt: {english_prompt}")  # 디버깅용 출력
    response = openai.images.generate(
        prompt=english_prompt,
        size="512x512"
    )
    image_url = response.data[0].url
    print(f"Generated image URL: {image_url}")  # 디버깅용 출력
    return image_url