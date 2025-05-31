import streamlit as st
from report_service import handle, eyes_report, generate_eyes_image
from eyes_info import search
from streamlit_option_menu import option_menu
from ui import ChatUI

# 챗봇 기능
def chatbot_ui():
    st.header("뷰티 챗봇 보우나")
    if "system_prompt_sent" not in st.session_state:
        st.session_state.system_prompt_sent = False

    chat_ui = ChatUI()
    chat_ui.render_chat_history()

    query = st.chat_input("메이크업이 고민된다면 편하게 말해주세요!")
    if query:
        handle(query)

# 보고서 기능
def report_ui():
    st.header("AI 뷰티 보고서")
    eyes_code = st.text_input("EYES_code를 입력하세요:")

    # 검색 버튼
    if st.button("검색"):
        if eyes_code:
            with st.spinner("E.Y.E.S 코드를 분석 중입니다..."):
                concept_desc = eyes_report(eyes_code)
                st.markdown(f"{eyes_code} 코드란?")
                st.markdown(concept_desc)
                
                img3 = generate_eyes_image(concept_desc)
                st.image(img3)
                
            result_df = search(eyes_code)
            if not result_df.empty:
                st.success(f"총 {len(result_df)}건의 결과가 있습니다.")
                # 표를 markdown으로 렌더링하여 url이 하이퍼링크로 보이도록
                st.markdown(
                    result_df.to_markdown(index=False), 
                    unsafe_allow_html=True
                )
            else:
                st.warning("해당 EYES_code에 해당하는 데이터가 없습니다.")
        else:
            st.info("EYES_code를 입력해주세요.")

# 즐겨찾기 기능
def favorites_ui():
    st.header("⭐ 즐겨찾기")
    favorites = ["펜슬 제품1", "펜슬 제품2", "펜슬 제품3"]
    for item in favorites:
        st.write(f"🔖 {item}")


# 사이드바 메뉴
with st.sidebar:
    choice = option_menu("메뉴", ["뷰티 상담봇", "AI 뷰티 보고서", "즐겨찾기"],
                         icons=['bi bi-robot', 'kanban', 'star'],
                         menu_icon="menu-app", default_index=0,
                         styles={
        "container": {"padding": "4!important", "background-color": "#fafafa"},
        "icon": {"color": "black", "font-size": "25px"},
        "nav-link": {"font-size": "16px", "text-align": "left", "margin":"0px", "--hover-color": "#fafafa"},
        "nav-link-selected": {"background-color": "#DAC5E2"},
    }
    )
    
# 메뉴에 따라 오른쪽 본문 렌더링
if choice == "뷰티 상담봇":
    chatbot_ui()
elif choice == "AI 뷰티 보고서":
    report_ui()
elif choice == "즐겨찾기":
    favorites_ui()