import streamlit as st
from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI

# .env 파일에서 환경 변수 로드
load_dotenv()

# OpenAI API 키 설정
openai_api_key = os.getenv("OPENAI_API_KEY")

# OpenAI 챗봇 모델 초기화
chat_model = ChatOpenAI(openai_api_key=openai_api_key)

# Streamlit 애플리케이션 설정
st.title("인공지능 시인")
subject = st.text_input("시의 주제를 입력해주세요.")
st.write("시의 주제 : " + subject)

if st.button("시 작성"):
    if subject:
        with st.spinner("시 작성중 ..."):
            try:
                result = chat_model.invoke(subject + "에 대한 시를 써줘.")
                st.write(result.content)
            except Exception as e:
                st.error(f"오류가 발생했습니다: {e}")
    else:
        st.error("시의 주제를 입력해주세요.")
