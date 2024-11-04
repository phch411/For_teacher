import streamlit as st
from datetime import date


st.title("🎈 명덕초 결석계 만들기")
st.write(
    "아래의 순서에 따라 만들어 봅시다."
)

# 이름 입력창 생성
st.text_input('이름을 입력하세요', '')


# 학년 옵션 리스트 생성
grades = [
    '1학년', '2학년', '3학년', '4학년', '5학년', '6학년'
]

# 선택창 생성
selected_grade = st.selectbox('학년을 선택하세요:', grades)

# 반 옵션 리스트 생성
classes = [
    '1반', '2반'
]

# 반 선택창 생성
selected_class = st.selectbox('반을 선택하세요:', classes)

# 번호 입력창 생성
number = st.number_input('번호를 입력하세요', min_value=1, step=1, value=1)

# 시작날짜 선택창 생성
start_date = st.date_input("시작날짜를 선택하세요", date.today())

# 끝 날짜 선택창 생성
end_date = st.date_input("끝나는 날짜를 선택하세요", date.today())

# 세부사항 옵션 리스트 생성
reasons = [
    '출석인정', '질병', '기타', '미인정'
]

# 선택창 생성
selected_reason = st.selectbox('결석 세부사항을 선택하세요:', reasons)