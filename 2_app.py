import streamlit as st
import pandas as st_pandas # 보통 import pandas as pd 로 사용하지만, 충돌 방지를 위해 명시
import pandas as pd
import numpy as np

# 페이지 기본 설정 (옵션)
st.set_page_config(page_title="데이터와 친해지기", page_icon="📈")

st.title("📈 Streamlit으로 데이터 시각화하기")
st.write("Streamlit은 데이터 분석가들에게 마법 같은 도구입니다. 복잡한 웹 코드 없이도 데이터를 표와 차트로 멋지게 보여줄 수 있거든요!")

st.divider()

# --- 1. 샘플 데이터 준비 ---
st.header("1. 데이터프레임 띄우기")
st.write("먼저, 가상의 상반기 지점별 매출 데이터를 만들어보겠습니다.")

# Pandas를 이용해 간단한 데이터프레임 생성
data = {
    '월': ['1월', '2월', '3월', '4월', '5월', '6월'],
    '서울지점': [150, 200, 250, 300, 280, 350],
    '부산지점': [120, 180, 200, 220, 260, 290],
    '제주지점': [80, 90, 110, 150, 140, 180]
}
df = pd.DataFrame(data)
df = df.set_index('월') # '월' 컬럼을 인덱스(기준)로 설정

# st.dataframe vs st.table의 차이점 보여주기
col1, col2 = st.columns(2) # 화면을 반으로 나누어 비교 (버전 3의 맛보기)

with col1:
    st.subheader("인터랙티브 표 (`st.dataframe`)")
    st.write("정렬, 스크롤, 크기 조절이 가능합니다.")
    st.dataframe(df, use_container_width=True)

with col2:
    st.subheader("고정된 표 (`st.table`)")
    st.write("깔끔하게 고정된 형태로 출력됩니다.")
    st.table(df)

st.divider()

# --- 2. 핵심 지표 (Metrics) 강조하기 ---
st.header("2. 주요 지표(Metric) 한눈에 보기")
st.write("대시보드 상단에 자주 들어가는 요약 정보입니다.")

# 3개의 컬럼으로 나누어 지표 표시
m1, m2, m3 = st.columns(3)
m1.metric(label="서울지점 6월 매출", value="350만 원", delta="70만 원") # delta: 이전 대비 증감
m2.metric(label="부산지점 6월 매출", value="290만 원", delta="30만 원")
m3.metric(label="제주지점 6월 매출", value="180만 원", delta="40만 원")

st.divider()

# --- 3. 차트 그리기와 인터랙션 ---
st.header("3. 차트 시각화 및 데이터 필터링")
st.write("데이터프레임을 그대로 차트 함수에 넣기만 하면 그래프가 완성됩니다.")

# 수강생들이 직접 조작해 볼 수 있는 멀티셀렉트(다중 선택) 위젯 추가
selected_branches = st.multiselect(
    "📊 그래프로 확인할 지점을 선택하세요:",
    ['서울지점', '부산지점', '제주지점'],
    default=['서울지점', '부산지점'] # 기본으로 선택되어 있을 항목
)

# 선택된 지점의 데이터만 필터링하여 차트 그리기
if selected_branches:
    filtered_df = df[selected_branches]
    
    st.subheader("📉 꺾은선 그래프 (Line Chart)")
    st.line_chart(filtered_df)
    
    st.subheader("📊 막대 그래프 (Bar Chart)")
    st.bar_chart(filtered_df)
else:
    # 아무것도 선택하지 않았을 때의 경고 메시지
    st.info("선택된 지점이 없습니다. 위의 박스에서 지점을 하나 이상 선택해 주세요.")