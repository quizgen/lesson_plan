import streamlit as st
import openai
from dotenv import load_dotenv
import os

# .env 파일에서 환경 변수 로드
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def generate_poem(topic):
    prompt = f"{topic}에 대한 시를 한국어로 작성해줘"

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a poet."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=150,
        temperature=0.7,
    )

    poem = response.choices[0].message["content"].strip()
    return poem


st.title("AI 시인 챗봇")
st.write("주제를 입력하면 AI가 시를 작성합니다.")

# 사용자로부터 주제 입력받기
topic = st.text_input("시의 주제를 입력하세요")

if st.button("시 생성하기"):
    if topic:
        with st.spinner("시를 생성하는 중입니다..."):
            try:
                poem = generate_poem(topic)
                st.success("생성된 시:")
                st.write(poem)
            except Exception as e:
                st.error(f"오류가 발생했습니다: {e}")
    else:
        st.error("시의 주제를 입력해주세요")
