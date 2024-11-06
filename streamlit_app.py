import streamlit as st
from datetime import date, timedelta
from docxtpl import DocxTemplate 
import io
import streamlit.components.v1 as components




def calculate_absence_period(start_date, end_date):
    return (end_date - start_date).days + 1  # 끝 날짜도 포함하므로 1을 더합니다

def adjust_date(end_date):
    # 3일 추가
    new_date = end_date + timedelta(days=3)
    # 주말인지 체크
    if new_date.weekday() == 5:  # 토요일
        new_date += timedelta(days=2)  # 월요일로 설정
    elif new_date.weekday() == 6:  # 일요일
        new_date += timedelta(days=1)  # 월요일로 설정
    return new_date

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
    st.session_state.name = st.text_input('이름을 입력하세요', st.session_state.name)
    
    grades = ['1', '2', '3', '4', '5', '6']
    st.session_state.selected_grade = st.selectbox('학년을 선택하세요:', grades, index=grades.index(st.session_state.selected_grade))
    
    classes = ['1', '2']
    st.session_state.selected_class = st.selectbox('반을 선택하세요:', classes, index=classes.index(st.session_state.selected_class))
    
    st.session_state.student_num = st.number_input('번호를 입력하세요', min_value=1, step=1, value=st.session_state.student_num)
    
    st.session_state.start_date = st.date_input("시작날짜를 선택하세요", st.session_state.start_date)
    st.session_state.end_date = st.date_input("끝나는 날짜를 선택하세요", st.session_state.end_date)
    
    details = ['출석인정', '질병', '기타', '미인정']
    st.session_state.selected_details = st.selectbox('결석 세부사항을 선택하세요:', details, index=details.index(st.session_state.selected_details))

    st.session_state.reason = st.text_input('사유를 입력하세요', st.session_state.reason)


if st.session_state.start_date <= st.session_state.end_date:
    absence_period = calculate_absence_period(st.session_state.start_date, st.session_state.end_date)
    st.write(f"결석 시작일: {st.session_state.start_date}")
    st.write(f"결석 종료일: {st.session_state.end_date}")
    st.write(f"총 결석 기간: {absence_period}일")
else:
    st.error("종료 날짜는 시작 날짜보다 늦어야 합니다.")



# 결석계 생성 버튼
if st.button("결석계 생성"):
    if st.session_state.name and st.session_state.selected_grade and st.session_state.selected_class and st.session_state.student_num and st.session_state.start_date <= st.session_state.end_date:
        absence_period = calculate_absence_period(st.session_state.start_date, st.session_state.end_date)
        today = adjust_date(st.session_state.end_date)
        context = {
            'name': st.session_state.name,
            'grade': st.session_state.selected_grade,
            'class': st.session_state.selected_class,
            'number': st.session_state.student_num,
            'start_date': st.session_state.start_date.strftime("%Y년 %m월 %d일"),
            'end_date': st.session_state.end_date.strftime("%Y년 %m월 %d일"),
            'days': absence_period,
            'details': st.session_state.selected_details,
            'reason': st.session_state.reason,
            'today': today.strftime("%Y년 %m월 %d일")
        }
        
        doc_io = create_absence_note(context)
        
         # 다운로드 버튼 생성
        st.download_button(
            label="결석계 다운로드",
            data=doc_io,
            file_name=f"{st.session_state.name}_결석계.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
        st.success(f"결석계가 생성되었습니다. 오늘 날짜는 {today.strftime('%Y년 %m월 %d일')}로 설정되었습니다.")

        if st.button("프린터 출력"):
            components.html(
                """
                <script>
                function printPage() {
                window.print()
                }
                </script>
                <button onclick="printPage()">프린터로 출력</button>
                """,
                height=50
            )
    else:
        st.error("모든 필드를 올바르게 입력해주세요.")

# 주의사항 수정
st.info("주의: 결석계 템플릿 파일(.docx)을 먼저 업로드해주세요.")