import streamlit as st
import pandas as pd

# 페이지 설정 (가장 위에 작성해야 합니다)
# layout="wide"를 사용하면 화면을 넓게 쓸 수 있어 대시보드에 적합합니다.
st.set_page_config(page_title="레이아웃 마스터", page_icon="📱", layout="wide")

# --- 1. 사이드바 (Sidebar) 구성 ---
# st.sidebar를 붙이면 왼쪽에 숨길 수 있는 메뉴바가 생깁니다.
st.sidebar.title("⚙️ 설정 메뉴")
st.sidebar.write("사이드바에서 옵션을 제어해보세요.")

# 사이드바에 위젯 넣기
user_theme = st.sidebar.radio("앱 테마 느낌(가상)", ["기본", "다크 모드", "라이트 모드"])
show_data = st.sidebar.checkbox("상세 데이터 보기", value=True)

st.sidebar.divider()
st.sidebar.info("💡 팁: 사이드바에는 주로 페이지 이동 메뉴나 데이터 필터링 옵션을 넣습니다.")

# --- 메인 화면 시작 ---
st.title("📱 앱을 앱답게: 레이아웃 마스터하기")
st.write("화면을 나누고 탭을 추가하면 훨씬 전문적인 웹 애플리케이션처럼 보입니다.")

# --- 2. 탭 (Tabs) 구성 ---
# 한 화면 공간을 효율적으로 쓰기 위해 탭을 만듭니다.
tab1, tab2, tab3 = st.tabs(["📊 대시보드", "📝 상세 데이터", "✨ 기타 기능"])

# 첫 번째 탭 내용
with tab1:
    st.header("메인 대시보드")
    
    # --- 3. 단 나누기 (Columns) ---
    # 화면을 3개의 열로 쪼갭니다.
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("오늘의 방문자", "1,024명", "12명")
    with col2:
        st.metric("이번 주 수익", "5,230,000원", "300,000원")
    with col3:
        st.metric("고객 만족도", "4.8/5.0", "0.1")
        
    st.success("`st.columns()`를 사용하면 위젯이나 차트를 가로로 나란히 배치할 수 있습니다!")

# 두 번째 탭 내용
with tab2:
    st.header("상세 데이터 확인")
    
    # 사이드바의 체크박스 상태에 따라 내용을 보여주거나 숨깁니다.
    if show_data:
        # 가상의 데이터
        sample_data = pd.DataFrame({
            "이름": ["김철수", "이영희", "박지민"],
            "부서": ["영업팀", "마케팅팀", "개발팀"],
            "실적": [85, 92, 78]
        })
        st.dataframe(sample_data, use_container_width=True)
    else:
        st.warning("👈 왼쪽 사이드바에서 '상세 데이터 보기'를 체크해주세요.")

# 세 번째 탭 내용
with tab3:
    st.header("공간 절약하기")
    
    # --- 4. 접기/펴기 (Expander) ---
    with st.expander("클릭해서 숨겨진 도움말 보기 🔽"):
        st.write("이 공간은 평소에는 접혀 있어서 화면을 깔끔하게 유지해 줍니다.")
        st.write(f"참고로, 현재 사이드바에서 선택하신 테마는 **{user_theme}**입니다.")
        st.button("설정 저장하기")