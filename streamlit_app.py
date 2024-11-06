import streamlit as st
from datetime import date
from docxtpl import DocxTemplate 
import io




def calculate_absence_period(start_date, end_date):
    return (end_date - start_date).days + 1  # 끝 날짜도 포함하므로 1을 더합니다


# 문서 생성 함수
def create_absence_note(context):
    doc = DocxTemplate("2024. 결석신고서 양식.docx")  # 템플릿 파일 이름
    doc.render(context)
    doc_io = io.BytesIO()
    doc.save(doc_io)
    doc_io.seek(0)
    return doc_io

# 세션 상태 초기화
if 'name' not in st.session_state:
    st.session_state.name = ''
if 'selected_grade' not in st.session_state:
    st.session_state.selected_grade = '1'
if 'selected_class' not in st.session_state:
    st.session_state.selected_class = '1'
if 'student_num' not in st.session_state:
    st.session_state.student_num = 1
if 'start_date' not in st.session_state:
    st.session_state.start_date = date.today()
if 'end_date' not in st.session_state:
    st.session_state.end_date = date.today()
if 'selected_details' not in st.session_state:
    st.session_state.selected_details = '출석인정'
if 'reason' not in st.session_state:
    st.session_state.reason = ''

st.title("🎈 명덕초 결석계 만들기")
st.write(
    "아래의 순서에 따라 만들어 봅시다."
)
with st.sidebar:

    # 이름 입력창 생성
    name = st.text_input('이름을 입력하세요', '')


    # 학년 옵션 리스트 생성
    grades = [
        '1', '2', '3', '4', '5', '6'
    ]

    # 선택창 생성
    selected_grade = st.selectbox('학년을 선택하세요:', grades)

    # 반 옵션 리스트 생성
    classes = [
        '1', '2'
    ]

    # 반 선택창 생성
    selected_class = st.selectbox('반을 선택하세요:', classes)

    # 번호 입력창 생성
    student_num = st.number_input('번호를 입력하세요', min_value=1, step=1, value=1)

    # 시작날짜 선택창 생성
    start_date = st.date_input("시작날짜를 선택하세요", date.today())

    # 끝 날짜 선택창 생성
    end_date = st.date_input("끝나는 날짜를 선택하세요", date.today())

# 기간 알리는 창 만들기
if start_date <= end_date:
    # 결석 기간 계산
    absence_period = calculate_absence_period(start_date, end_date)
    
    # 결과 표시
    st.write(f"결석 시작일: {start_date}")
    st.write(f"결석 종료일: {end_date}")
    st.write(f"총 결석 기간: {absence_period}일")
else:
    st.error("종료 날짜는 시작 날짜보다 늦어야 합니다.")

# 세부사항 옵션 리스트 생성
details = [
    '출석인정', '질병', '기타', '미인정'
]

# 선택창 생성
selected_details = st.selectbox('결석 세부사항을 선택하세요:', details)

# 사유 입력창 생성
reason = st.text_input('사유를 입력하세요')



# 결석계 생성 버튼
if st.button("결석계 생성"):
    if name and selected_grade and selected_class and student_num and start_date <= end_date:
        context = {
            'name': name,
            'grade': selected_grade,
            'class': selected_class,
            'number': student_num,
            'start_date': start_date.strftime("%Y년 %m월 %d일"),
            'end_date': end_date.strftime("%Y년 %m월 %d일"),
            'days': absence_period,
            'details': selected_details,
            'reason': reason
        }
        
        doc_io = create_absence_note(context)
        
         # 다운로드 버튼 생성
        st.download_button(
            label="결석계 다운로드",
            data=doc_io,
            file_name=f"{name}_결석계.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
    else:
        st.error("모든 필드를 올바르게 입력해주세요.")

# 주의사항 수정
st.info("주의: 결석계 템플릿 파일(.docx)을 먼저 업로드해주세요.")