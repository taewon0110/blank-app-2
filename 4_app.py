import streamlit as st
import time

st.set_page_config(page_title="동적 기능과 미디어", page_icon="🎬")
st.title("🎬 다양한 동적 기능과 미디어 활용")
st.write("단순한 데이터 출력을 넘어, 사용자와 상호작용하고 알림을 주는 기능들을 알아봅니다.")

st.divider()

# --- 1. 파일 업로드 및 카메라 ---
st.header("1. 미디어 입력 받기")
st.write("사용자의 PC나 스마트폰으로부터 직접 파일이나 사진을 입력받을 수 있습니다.")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📁 이미지 업로드")
    # 파일 업로더 위젯
    uploaded_file = st.file_uploader("이미지 파일을 올려보세요", type=['png', 'jpg', 'jpeg'])
    if uploaded_file is not None:
        st.image(uploaded_file, caption="업로드된 이미지", use_container_width=True)

with col2:
    st.subheader("📷 카메라 입력")
    # 웹캠 연동 위젯 (노트북 웹캠이나 스마트폰 카메라 활성화)
    picture = st.camera_input("사진을 찍어보세요")
    if picture:
        st.image(picture, caption="촬영된 사진", use_container_width=True)

st.divider()

# --- 2. 진행 상태 및 피드백 (로딩 효과) ---
st.header("2. 진행 상태 및 팝업 알림")
st.write("시간이 걸리는 작업을 할 때 사용자에게 진행 상황을 시각적으로 보여줍니다.")

if st.button("가상의 데이터 분석 시작"):
    # 1단계: 스피너 (빙글빙글 도는 로딩 애니메이션)
    with st.spinner('데이터를 불러오는 중입니다...'):
        time.sleep(1.5) # 실제로는 여기서 데이터 로딩 작업을 수행
    
    # 2단계: 프로그레스 바 (상태 진행률 표시)
    st.write("데이터 분석 진행 중...")
    progress_bar = st.progress(0)
    for i in range(100):
        time.sleep(0.02) # 짧은 지연 시간으로 게이지가 차오르는 효과
        progress_bar.progress(i + 1)
        
    st.success("분석이 완료되었습니다!")
    
    # 3단계: 토스트 알림 (우측 하단에 잠깐 떴다 사라지는 팝업)
    st.toast('✅ 작업이 성공적으로 끝났습니다!', icon='🎉')
    st.balloons()

st.divider()

# --- 3. 상태 유지 (Session State) ---
st.header("3. 데이터 기억하기 (Session State)")
st.write("Streamlit은 버튼을 누를 때마다 코드가 처음부터 다시 실행됩니다. 값을 기억하려면 `st.session_state`를 사용해야 합니다.")

# '좋아요' 카운트 변수가 세션에 없다면 0으로 초기화
if 'like_count' not in st.session_state:
    st.session_state.like_count = 0

# 버튼을 누르면 세션 상태의 카운트를 1 증가
if st.button("👍 이 기능이 마음에 들어요!"):
    st.session_state.like_count += 1

# 누적된 카운트 출력
st.write(f"현재 누적된 좋아요 수: **{st.session_state.like_count}** 개")