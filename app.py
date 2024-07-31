import streamlit as st
from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
import pandas as pd

# .env 파일에서 환경 변수 로드
load_dotenv()

# OpenAI API 키 설정
openai_api_key = os.getenv("OPENAI_API_KEY")

# OpenAI 챗봇 모델 초기화
chat_model = ChatOpenAI(openai_api_key=openai_api_key, model_name="gpt-4o")


# 수업계획서 생성 함수
def generate_syllabus(subject_name, course_overview, course_objectives):
    prompt = f"""
    너는 수업계획서 작성 전문가이다. 다음 정보를 바탕으로 수업계획서를 표로만 작성해줘:
    과목명: {subject_name}
    교과목 개요: {course_overview}
    수업목표: {course_objectives}

    <포맷예시>
    주차\t보강시 예정일\t강의주제 및 내용\t강의방법
    1주\t\t일반수업활동 : 강의 개요 xcode 사용\tT PT P D
    """
    response = chat_model.invoke(prompt)
    return response.content.strip()


# 생성된 수업계획서를 DataFrame으로 변환하는 함수
def parse_syllabus(syllabus_text):
    lines = syllabus_text.split("\n")
    data = []
    for line in lines[1:]:
        if line.strip() and "|" in line:
            columns = [col.strip() for col in line.split("|")[1:-1]]
            data.append(columns)
    df = pd.DataFrame(
        data, columns=["주차", "보강시 예정일", "강의주제 및 내용", "강의방법"]
    )
    return df


# Streamlit 애플리케이션 설정
st.title("수업계획서 생성기")

# 사용자 입력 받기
subject_name = st.text_input("과목명을 입력해주세요.")
course_overview = st.text_area("교과목 개요를 입력해주세요.")
course_objectives = st.text_area("수업목표를 입력해주세요.")

# 수업계획서 생성 버튼
if st.button("수업계획서 생성"):
    if subject_name and course_overview and course_objectives:
        with st.spinner("수업계획서 생성중 ..."):
            try:
                syllabus_text = generate_syllabus(
                    subject_name, course_overview, course_objectives
                )
                st.subheader("생성된 수업계획서")

                # 수업계획서를 DataFrame으로 변환하여 표시
                syllabus_df = parse_syllabus(syllabus_text)
                st.table(syllabus_df)

                # 강의방법 코드 설명 표시
                st.markdown(
                    """
                **강의방법 코드:**
                - **T**: 이론 강의
                - **PT**: 실습 강의
                - **P**: 프로젝트
                - **D**: 토론
                - **EXAM**: 시험
                """
                )

            except Exception as e:
                st.error(f"오류가 발생했습니다: {e}")
    else:
        st.error("모든 입력값을 채워주세요.")
