import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import io

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# T-Protocol 로딩: 가식 없는 팩트폭격 카페 시뮬레이터 (매운맛)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.set_page_config(
    page_title="☕ 메가급 저가커피 창업 시뮬레이터",
    page_icon="☕",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@300;400;500;700;900&display=swap');
html, body, [class*="css"] { font-family: 'Noto Sans KR', sans-serif; }
.kpi-card { background: linear-gradient(135deg, #18181b 0%, #27272a 100%); border: 1px solid #3f3f46; border-radius: 12px; padding: 20px; transition: all 0.3s; }
.kpi-card:hover { border-color: #ef4444; box-shadow: 0 4px 20px rgba(239, 68, 68, 0.2); }
.kpi-title { font-size: 0.85rem; color: #a1a1aa; font-weight: 700; margin-bottom: 5px; }
.kpi-val { font-size: 1.8rem; font-weight: 900; color: #f4f4f5; font-family: monospace; }
.fact-box { border-left: 4px solid #FCD34D; background: #27272a; padding: 15px; margin: 15px 0; border-radius: 0 8px 8px 0; }
.fact-title { color: #FCD34D; font-weight: 900; font-size: 1.1rem; margin-bottom: 5px; }
.fact-text { color: #d4d4d8; font-size: 0.95rem; line-height: 1.5; }
.header-container { background: linear-gradient(135deg, #1C1914 0%, #2A251D 100%); padding: 35px 40px; border-radius: 16px; border: 1px solid rgba(252, 211, 77, 0.3); box-shadow: 0 10px 40px -10px rgba(252, 211, 77, 0.2); margin-bottom: 30px; position: relative; overflow: hidden; }
.header-container::before { content: ''; position: absolute; top: -50%; left: -50%; width: 200%; height: 200%; background: radial-gradient(circle, rgba(252, 211, 77, 0.05) 0%, transparent 60%); }
.tprot-badge { display: inline-block; background: rgba(252, 211, 77, 0.15); border: 1px solid rgba(252, 211, 77, 0.5); color: #FCD34D; padding: 6px 14px; border-radius: 20px; font-size: 0.8rem; font-weight: 700; margin-bottom: 15px; letter-spacing: 0.5px; }
.tprot-title { color: #fff; font-size: 2.2rem; font-weight: 900; margin: 0 0 12px 0; letter-spacing: -1.2px; line-height: 1.2; text-shadow: 0 2px 10px rgba(0, 0, 0, 0.5); }
.tprot-title span { color: #FCD34D; }
.tprot-subtitle { color: #a1a1aa; font-size: 1.05rem; font-weight: 400; margin: 0; line-height: 1.6; }
h3 { margin-top: 1.5rem; }
.stSlider > div > div > div > div { background-color: #FCD34D; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="header-container">
    <div class="tprot-badge">☕ MEGA-PROTOCOL EXCLUSIVE</div>
    <h1 class="tprot-title">🟡 메가급 저가커피 브랜드 실전 <span>재무 진단기</span></h1>
    <p class="tprot-subtitle">프랜차이즈 본사 영업사원은 절대 말해주지 않는 가맹점 실질 수익률(Margin)과 단위경제학(Unit Economics) 팩트 체크.</p>
</div>
""", unsafe_allow_html=True)

# ── 데이터셋 ──
# 회전율 = 평수당 하루 샤 수량 (저가커피는 테이크아웃 미마씨, 회전율 실질적 지표는 좌석주 3주기 아니라 평수당 일평균 주문수)
LOCATIONS = {
    "S급 (메인상권)": {"보증금평당": 350, "월세평당": 25, "권리금평당": 400, "회전율": 18.0, "인테리어": 450},
    "A급 (번화가)": {"보증금평당": 250, "월세평당": 15, "권리금평당": 200, "회전율": 13.0, "인테리어": 350},
    "B급 (오피스/대학가)": {"보증금평당": 150, "월세평당": 10, "권리금평당": 100, "회전율": 9.0, "인테리어": 280},
    "C급 (동네 구석)": {"보증금평당": 100, "월세평당": 6, "권리금평당": 20, "회전율": 3.5, "인테리어": 200},
}

with st.sidebar:
    st.header("⚡ 원클릭 자동 팩트 세팅 (2026년형)")
    
    if "loc_sel" not in st.session_state:
        st.session_state.update({
            "loc_sel": "B급 (오피스/대학가)", "area": 15, "unit_price": 5000, 
            "mat_ratio": 35, "del_ratio": 20, "owner_hrs": 10, "alba_count": 1.5,
            "pt_wage": 12500, "black_consumer": 2.5, "alba_run": 15,
            "gov_subsidy": 0, "use_youth_loan": False
        })
        
    def apply_preset():
        p = st.session_state.preset_radio
        if "1%" in p:
            # A급 번화가 15평, 알바 최소화(1명), 점주 주도 오퍼레이션, 정부지원 풀 활용
            st.session_state.loc_sel = "A급 (번화가)"
            st.session_state.area = 15
            st.session_state.unit_price = 5500
            st.session_state.mat_ratio = 30
            st.session_state.del_ratio = 0
            st.session_state.owner_hrs = 12   # 점주 12시간 풀매대 전담
            st.session_state.alba_count = 1.0 # 알바 최소 1명 유지
            st.session_state.pt_wage = 14000
            st.session_state.black_consumer = 0.5
            st.session_state.alba_run = 0
            st.session_state.gov_subsidy = 4500
            st.session_state.use_youth_loan = True
        elif "평균" in p:
            # S급 메인상권에 들어갔지만 수익 안 나는 구조
            # 점주 16시간 뼈 갈리는데 오너 시급 < 최저임금 → 진짜 워킹푸어
            st.session_state.loc_sel = "S급 (메인상권)"
            st.session_state.area = 10
            st.session_state.unit_price = 2500   # 아이스 아메리카노 단일 저객단가
            st.session_state.mat_ratio = 40       # 로스율 포함 원가 40%
            st.session_state.del_ratio = 60       # 배달 외형만 불리기 60%
            st.session_state.owner_hrs = 16       # 점주 16시간 매대 혹사
            st.session_state.alba_count = 2.0     # 알바는 써야 돌아감 (최저시급)
            st.session_state.pt_wage = 9860       # 최저시급으로 갈아넣기
            st.session_state.black_consumer = 4.0 # 배달 많으니 진상 클레임 빈발
            st.session_state.alba_run = 50        # 최저시급이라 알바 이탈 잦음
            st.session_state.gov_subsidy = 0      # 정부지원 신청할 시간도 없음
            st.session_state.use_youth_loan = False

    st.radio("빅데이터 수집 기반 현실 프리셋", 
        ["사용자 커스텀 (수동 세팅)", "🔥 상위 1% S급 매장 (캐시카우)", "📉 대한민국 평균 일반 매장 (워킹푸어)"], 
        index=0, key="preset_radio", on_change=apply_preset)
        
    st.divider()

    st.header("1️⃣ 입지 및 투자비용 (CAPEX)")
    loc_sel = st.selectbox("상권 수준 (현실 파악부터)", list(LOCATIONS.keys()), key="loc_sel")
    area = st.number_input("매장 평수", min_value=10, max_value=100, key="area")
    loc = LOCATIONS[loc_sel]
    
    dep = st.number_input("보증금 (만원)", 0, 100000, int(loc['보증금평당']*area), step=100)
    kwon = st.number_input("바닥/영업 권리금 (만원) - 날릴 확률 농후", 0, 50000, int(loc['권리금평당']*area), step=100)
    rent = st.number_input("월세 (만원) - 비가 오나 눈이 오나 나감", 0, 5000, int(loc['월세평당']*area), step=10)
    
    st.divider()
    st.header("2️⃣ 매출 볼륨 및 원가 구조 (COGS)")
    unit_price = st.number_input("예상 평균 객단가 (원)", min_value=2000, max_value=20000, step=500, key="unit_price", help="저가커피는 아메리카노 1500~2000원이지만, 디저트/에이드 묶어파는 평균 객단가를 입력해라.")
    material_ratio = st.slider("원부자재 원가율 (%) - 본사 필수물대 포함", min_value=15, max_value=60, key="mat_ratio") / 100.0
    delivery_ratio = st.slider("배달 비중 (%) - 할수록 역마진 직행", min_value=0, max_value=80, key="del_ratio") / 100.0
    delivery_fee_ratio = st.slider("배달 플랫폼 수수료 및 부대비용 (%)", 10, 50, 25) / 100.0
    
    st.divider()
    st.header("3️⃣ 오퍼레이션 및 리스크 제어")
    work_hrs = 14
    owner_work = st.slider(f"가맹점주 상주시간 (일 기준, 총 {work_hrs}H 중)", min_value=0, max_value=16, key="owner_hrs")
    alba_count = st.slider("동시 근무 매니저/스태프 수 비율", min_value=0.5, max_value=4.0, step=0.5, key="alba_count", help="피크타임 샷 뽑는 노동 강도 고려. 메가급은 피크 때 3-4명도 갈아넣는다.")
    pt_wage = st.number_input("스태프 실질 시급 (주휴+퇴직금리스크 반영)", min_value=9860, max_value=20000, key="pt_wage")
    
    st.markdown("💸 **[오퍼레이션 정부지원 영끌]**")
    gov_job_subsidy = st.checkbox("청년일자리도약장려금 (스태프 1인당 월 인건비 보조)", value=False, help="2026년 기준 6개월 채용 유지 시 월 최대 60만원 인건비 보조율 삭감 적용.")
    gov_voucher = st.checkbox("소상공인 경영안정 바우처 (전기세 등 유지비 차감)", value=False, help="연 25만 원 상당의 경영 고정비 바우처를 월 단위 공과금에서 선차감한다.")

    st.markdown("🚨 **[운영 리스크 파라미터 (HR/CS/설비)]**")
    black_consumer = st.slider("강성 클레임 & 서비스 환불 손실률 (%)", min_value=0.0, max_value=10.0, step=0.1, key="black_consumer") / 100.0
    alba_run = st.number_input("인력 이탈 OJT 매몰비용 (구인/교육/결근 월 만원)", min_value=0, max_value=100, key="alba_run")
    machine_fail = st.number_input("에스프레소 머신/제빙기 등 설비 감가상각 (월 만원)", 0, 80, 15)
    
    st.divider()
    st.header("4️⃣ 자본 레버리지 (정책자금 & 금융비용)")
    my_cash = st.number_input("순수 자기 자본 (만원)", 0, 200000, 5000, step=1000)
    
    st.markdown("💸 **[2026년 소진공/중진공 정책자금 영끌]**")
    gov_subsidy = st.slider("중소벤처기업부 예비창업패키지 등 무상지원금 (상환X, 만원)", min_value=0, max_value=10000, step=500, key="gov_subsidy", help="2026년 예창패 등 청년 지원 평균 4,700만원. 갚지 않아도 되는 순수 국비 지원액.")
    use_youth_loan = st.checkbox("중소벤처기업진흥공단(중진공): 청년전용창업자금 대출 (최대 1억, 연 2.5% 고정)", key="use_youth_loan")
    use_sme_loan = st.checkbox("소상공인시장진흥공단(소진공): 일반경영안정자금 대출 (최대 7천만, 기본금리 -0.5%p 우대)", value=False)
    
    interest_rate_normal = st.number_input("1/2금융권 일반 사업자 대출 금리 (%)", 2.0, 15.0, 6.5, step=0.1) / 100.0

# ── 초기투자 (CAPEX: 메가커피 가맹 가이드라인 반영) ──
franchise_fee = 1000 # 본사 가맹비
edu_fee = 500 # 본사 교육비 및 OJT
contract_dep = 200 # 계약이행보증금
int_cost = loc['인테리어'] * area # 평당 인테리어 (철거, 전기증설, 냉난방 별도공사 포함)
machine_cost = 4000 # 고급 에스프레소 머신, 그라인더, 제빙기, 블렌더 등 기기설비
sign_etc_cost = 1000 # 내외부 간판(사인물), DID 메뉴보드, 키오스크 설치비 등
total_startup = dep + kwon + franchise_fee + edu_fee + contract_dep + int_cost + machine_cost + sign_etc_cost
total_funds_needed = max(0, total_startup - my_cash - gov_subsidy)

# ── 연산 ──
seats = int(area * 0.7) 
daily_cust_offline = seats * loc['회전율']
daily_cust_delivery = daily_cust_offline * (delivery_ratio / max(1 - delivery_ratio, 0.01))

daily_rev_offline = daily_cust_offline * unit_price
daily_rev_delivery = daily_cust_delivery * unit_price
monthly_rev = (daily_rev_offline + daily_rev_delivery) * 30

monthly_material = monthly_rev * material_ratio
monthly_delivery_fee = (daily_rev_delivery * 30) * delivery_fee_ratio

# 인건비
needed_labor_hours = work_hrs * alba_count 
alba_hours = max(0, needed_labor_hours - owner_work)
monthly_labor_raw = alba_hours * pt_wage * 30

hired_staff = int(alba_count + 0.99) if alba_count > 0 else 0
job_subsidy_amount = min(monthly_labor_raw, hired_staff * 600000) if gov_job_subsidy else 0
monthly_labor = monthly_labor_raw - job_subsidy_amount

# 고정 & 현실 반영 변동비
youth_loan_amt = min(total_funds_needed, 10000) if use_youth_loan else 0
rem_after_youth = max(0, total_funds_needed - youth_loan_amt)

sme_loan_amt = min(rem_after_youth, 7000) if use_sme_loan else 0
normal_loan_amt = max(0, rem_after_youth - sme_loan_amt)

sme_interest_rate = max(0, interest_rate_normal - 0.005) # 소진공 -0.5% 금리 우대 반영

monthly_interest = (youth_loan_amt * 0.025 / 12 * 10000) + (sme_loan_amt * sme_interest_rate / 12 * 10000) + (normal_loan_amt * interest_rate_normal / 12 * 10000)
loan_amt = youth_loan_amt + sme_loan_amt + normal_loan_amt

utility_raw = area * 60000 
utility = max(0, utility_raw - (250000 / 12)) if gov_voucher else utility_raw

card_fee = monthly_rev * 0.015
etc_fixed = 300000 

black_consumer_loss = monthly_rev * black_consumer # 진상 손님 손실액
hidden_risk_cost = (alba_run * 10000) + (machine_fail * 10000) + black_consumer_loss

total_cost = (rent*10000) + monthly_material + monthly_labor + monthly_delivery_fee + monthly_interest + utility + card_fee + etc_fixed + hidden_risk_cost
net_profit = monthly_rev - total_cost

owner_monthly_hours = owner_work * 30
owner_hourly_wage = net_profit / max(owner_monthly_hours, 1) if net_profit > 0 else 0

st.markdown("### 📊 T-Protocol 종합 재무 성적표 (현실 직시)")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f'<div class="kpi-card"><div class="kpi-title">총 창업비용 (초기 대출/자본금)</div><div class="kpi-val" style="color:#f87171">{total_startup:,}만</div></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="kpi-card"><div class="kpi-title">월 고정 유지비용 (Sunk Cost 등)</div><div class="kpi-val" style="color:#fbbf24">{int(((rent*10000) + monthly_interest + utility + etc_fixed + (machine_fail*10000))/10000):,}만</div></div>', unsafe_allow_html=True)
with col3:
    st.markdown(f'<div class="kpi-card"><div class="kpi-title">월 순수익 (실질 현금흐름)</div><div class="kpi-val" style="color:{"#4ade80" if net_profit>0 else "#ef4444"}">{int(net_profit/10000):,}만</div></div>', unsafe_allow_html=True)
with col4:
    color = "#4ade80" if owner_hourly_wage > pt_wage else "#ef4444"
    st.markdown(f'<div class="kpi-card"><div class="kpi-title">오너 실질 시급 (기회비용 대비)</div><div class="kpi-val" style="color:{color}">{int(owner_hourly_wage):,}원</div></div>', unsafe_allow_html=True)

st.markdown("---")

# T-Protocol 핵심 재무 진단 (Fact Check)
if net_profit < 0:
    st.markdown(f"""<div class="fact-box">
        <div class="fact-title">🚨 데스 스파이럴(Death Spiral) 진입. 구조적 파산 카운트다운 🚨</div>
        <div class="fact-text">매월 <b>{int(abs(net_profit)/10000):,}만 원</b>의 치명적 캐시번(Cash Burn)이 발생 중이다. 
        저가커피 씬에서 박리다매가 무너지면서 본사 물대와 배달앱 수수료만 감당하다가 점주가 말라죽는 전형적인 폐업 루트를 밟았다. 
        대출 돌려막기 같은 희망회로는 당장 접고, 긴급 메뉴 구조조정과 다운사이징 혹은 매장 양도(손절매)를 결단해라.<br><br>
        <span style="color:#34d399;"><b>🌱 [T-Protocol 비상 대책]</b> 단, 매몰비용이 아까워 돌이킬 수 없다면 당장 하단의 '비상 경영 처방전'을 읽고 피 흐르는 혈관부터 묶어라. 냉정한 메타인지가 생존의 시작이다.</span></div>
    </div>""", unsafe_allow_html=True)
elif owner_hourly_wage < pt_wage:
    st.markdown(f"""<div class="fact-box" style="border-color:#fbbf24;">
        <div class="fact-title">⚠️ 한계 기업 상태. 점주 노동력 착취(워킹푸어)를 통한 강제 흑자 ⚠️</div>
        <div class="fact-text">월 <b>{owner_monthly_hours}시간</b>의 오너 노동력을 갈아넣어 간신히 맞춘 순이익이 <b>{int(net_profit/10000):,}만 원</b>이다. 
        프랜차이즈가 자랑하는 뛰어난 가성비를 점주의 피와 땀으로 메우고 있다. 오너 실질 시급액 <b>{int(owner_hourly_wage):,}원</b>은 매대 닦는 알바(기본 {pt_wage}원)보다 못한 최악의 단가다. 
        시스템이 일하게 만들지 못하면 넌 본사 배나 불려주는 고도화된 스팀 노예일 뿐이다. 당장 아웃바운드 세일즈나 판관비 조정에 들어가라.</div>
    </div>""", unsafe_allow_html=True)
else:
    recoup_target = total_startup - gov_subsidy
    months_to_rec = (recoup_target * 10000) / net_profit
    if net_profit >= 10000000 or months_to_rec <= 24:
        st.markdown(f"""<div class="fact-box" style="border-color:#3b82f6;">
            <div class="fact-title">📈 엑설런트 박리다매! 압도적 볼륨(Volume) 강점 확보 📈</div>
            <div class="fact-text">저가형 프랜차이즈의 로망인 '터지는 회전율'을 달성했다. 월 순수익 <b>{int(net_profit/10000):,}만 원</b>에 투자금(부채+자본) 회수율 <b>{months_to_rec/12:.1f}년 ({int(months_to_rec)}개월)</b>이라는 메가급 초고속 캐시카우를 구축했다. 
            진상 고객 한두 명(월 <b>{int(black_consumer_loss/10000):,}만 원</b> 손실)이나 알바 교체비용 정도는 거뜬히 씹어먹는 규모의 경제를 입증했다. 
            현재 시스템과 인적 자원을 고도화시켜 인근 상권에 2호점 출점(다점포 전개)을 준비하는 등 자본 스케일업을 도모해라!</div>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""<div class="fact-box" style="border-color:#4ade80;">
            <div class="fact-title">✅ 영업이익권 진입 완료. 운영 최적화(Optimization) 방어전 돌입 ✅</div>
            <div class="fact-text">치열한 마진 싸움 끝에 <b>{int(net_profit/10000):,}만 원</b>의 영업 흑자 방어선을 뚫어냈다. 
            그러나 박리다매 구조에서 가장 무서운 건 슬로우 시즌 타격이나 예기치 못한 제빙기 고장(월 <b>{(alba_run+machine_fail):,}만 원</b> 소요) 같은 유동성 변수다. 
            현재 수익 흐름 기준 초기 환수 대상 자본금 <b>{recoup_target:,}만 원</b> 완전 회수까지 <b>{months_to_rec/12:.1f}년 ({int(months_to_rec)}개월)</b>이 예상된다. 경쟁 저가 커피 브랜드 기습 입점에 대비해 내부 사내유보금을 즉시 쌓아라.</div>
        </div>""", unsafe_allow_html=True)

c1, c2 = st.columns([1, 1.2])

with c1:
    st.markdown("### 📉 고정비 및 변동비 누수 구조 (Cost Breakdown)")
    df_cost = pd.DataFrame({
        "원인": ["임대료(고정)", "식자재원가", "인건비", "배달플랫폼 수수료액", "운영/CS리스크(이탈/클레임)", "일반부대비용액", "금융이자비용액"],
        "금액": [rent*10000, monthly_material, monthly_labor, monthly_delivery_fee, hidden_risk_cost, card_fee + utility + etc_fixed, monthly_interest]
    })
    fig_pie = px.pie(df_cost, names="원인", values="금액", hole=0.3, color_discrete_sequence=px.colors.sequential.YlOrRd_r)
    fig_pie.update_layout(paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#d4d4d8"), height=380, legend=dict(orientation="h", y=-0.2))
    st.plotly_chart(fig_pie, use_container_width=True)

with c2:
    st.markdown("### 🎲 리스크 매트릭스: 악성 클레임 vs 핵심인력 이탈")
    st.caption("고객 서비스(CS) 컴플레인율 도약 및 핵심 인력 이탈 시 실제 재무제표에 타격되는 순이익 시뮬레이션")
    
    alba_loss_arr = [0, 150000, 300000, 500000, 800000] # 알바 손실비
    bc_rate_arr = [0.0, 0.02, 0.05, 0.08, 0.12]         # 진상 환불 0~12%
    
    z_data = []
    for al in alba_loss_arr:
        row = []
        for bc in bc_rate_arr:
            c_loss = monthly_rev * bc
            h_loss = al + (machine_fail * 10000) + c_loss
            t_cost = (rent*10000) + monthly_material + monthly_labor + monthly_delivery_fee + monthly_interest + utility + card_fee + etc_fixed + h_loss
            row.append((monthly_rev - t_cost)/10000)
        z_data.append(row)
        
    fig_heat = go.Figure(data=go.Heatmap(
        z=z_data,
        x=[f"진상 {bc*100:.1f}%" for bc in bc_rate_arr],
        y=[f"알바손실 {int(al/10000)}만" for al in alba_loss_arr],
        colorscale="RdYlGn",
        text=[[f"{val:.0f}만" for val in r] for r in z_data],
        texttemplate="%{text}"
    ))
    fig_heat.update_layout(height=380, paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#e4e4e7"))
    st.plotly_chart(fig_heat, use_container_width=True)

st.divider()

st.markdown("### 💊 T-Protocol 생존 처방전: 수익률 강제 심폐소생술")
st.caption("니가 세팅한 데이터를 바탕으로 뽑아낸 팩트 기반 생존 전략이다. 피눈물 흘리기 전에 당장 실행해라.")

strategies = [
    {
        "trigger": monthly_rev > 0 and (rent*10000) / monthly_rev > 0.15,
        "title": f"임대료 임계치 초과 (Rent Burden: 현재 {rent*10000/max(monthly_rev,1)*100:.1f}%)",
        "text": "매출의 15% 이상이 고정 임대료로 소진되고 있다. 저단가 음료 씬에서는 '회전율이 곧 상가 월세'다. 매장 앞 키오스크로 워크인 고객 대기시간을 압축시켜 단위시간당 트래픽을 극대화하거나, 수익성 중심의 소형 테이크아웃 전용 B급 상권으로 상가 다운사이징(Downsizing)을 즉시 추진해라."
    },
    {
        "trigger": material_ratio > 0.35,
        "title": f"원부자재 코스트 과부하 (COGS: 현재 {material_ratio*100:.1f}%)",
        "text": "저가커피의 치명타인 본사 필수 물대 비중이 너무 높거나, 무분별한 레시피 로스(얼음/우유 폐기)로 마진이 붕괴됐다. 객단가 방어가 절급한 상태이므로 마진율이 60~70% 이상 보장되는 베이커리/마카롱 등의 고마진 사이드 메뉴 끼워팔기(Cross-selling) 프로모션을 매대에 강제 세팅해라."
    },
    {
        "trigger": delivery_ratio >= 0.30 and delivery_fee_ratio >= 0.20,
        "title": f"배달 채널 수익잠식 (Platform Dependency: 플랫폼 종속률 {delivery_fee_ratio*100:.1f}%)",
        "text": "저가 라인업 배달은 중개 수수료와 라이더 비용을 떼면 완벽한 역마진(적자) 산업이다. 매출 외형만 팽창할 뿐 실이익은 제로에 수렴한다. 배달 최소주문금액을 대폭 상향시켜 건당 객단가를 맞추고, 자사 앱(멤버십 오더)을 통한 패스트패스 픽업 유도로 오프라인 기반 포지션을 70%까지 강제 락인(Lock-in) 시켜라."
    },
    {
        "trigger": hidden_risk_cost > 500000,
        "title": f"운영 제반 리스크 관리 실패 (HR & CS Loss: 손실 누적 월 {int(hidden_risk_cost/10000)}만 도달)",
        "text": "아메리카노 머신처럼 갈려나가는 저가형 브랜드 오퍼레이션 특성상, 잦은 인원 공백과 메뉴 클레임은 폭발적인 OJT(교육) 매몰비용을 발생시킨다. 초보 스태프를 갈아끼우는 문화를 버리고, 시급을 높여서라도 '음료 추출과 컴플레인 전담' 매니저급 에이스를 배치해 이탈 원인을 통제하는 것이 압도적으로 저렴한 레버리지다."
    },
    {
        "trigger": owner_hourly_wage < pt_wage,
        "title": f"기회비용 상실형 오퍼레이션 (Low Owner ROI: 점주 실질 시급 {int(owner_hourly_wage)}원)",
        "text": f"오너가 샷 몇 십 잔 더 뽑아서 푼돈 아끼려다 월 {owner_monthly_hours}시간씩 매대에 묶여 체력만 고갈(최저임금 {pt_wage}원 미만 산출)시키고 있다. 저가커피 게임의 승패는 'B2B 볼륨'에 있다. 매장 로컬 운영은 파트타이머에게 일임하고, 점주는 당장 주변 오피스 밀집 구역이나 학원가로 튀어나가 대량 케이터링 정기 구독권(B2B)을 수주하는 아웃바운드 영업(Sales)에 사활을 걸어라."
    }
]

for s in strategies:
    if s["trigger"]:
        st.markdown(f'<div style="background:#1f191a; color:#ffffff; padding:15px; border-left:4px solid #f43f5e; margin-bottom:10px; border-radius:4px;">🩸 <b>{s["title"]}</b><br>{s["text"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div style="background:#27272a; color:#a1a1aa; padding:15px; border-left:4px solid #52525b; margin-bottom:10px; border-radius:4px;">✅ <del><b>{s["title"]}</b></del> (현재 수치상 방어 성공)<br><span style="font-size:0.9rem;">{s["text"]}</span></div>', unsafe_allow_html=True)

st.markdown("---")
st.markdown("### 🏆 [부록] 상위 1% vs 하위 10% 단위경제학 스터디 (Case Study)")
st.caption("비현실적 희망회로가 아닌, 냉정한 데이터를 바탕으로 완성된 S급 캐시카우 모델과 파산 모델의 비교 시뮬레이션이다.")

col_cs1, col_cs2 = st.columns(2)

with col_cs1:
    st.markdown("""
    <div style="background:#111113; border:1px solid #4ade80; border-radius:8px; padding:20px; height:100%;">
        <h4 style="color:#4ade80; margin-top:0;">🌟 S급 하이엔드 오퍼레이션 모델 (상위 1%)</h4>
        <ul style="color:#d4d4d8; font-size:0.95rem; line-height:1.7;">
            <li><b>전략적 입지:</b> '오피스/대학가 B급 상권'에서 임대료를 억제하고, 디저트 결합으로 <b>객단가를 6~8천 원 방어</b>한다.</li>
            <li><b>원가/플랫폼 락인:</b> 원가율 30% 이하 타겟팅. 매출 외형만 불리는 배달은 과감히 끊고 <b>자사앱 픽업 기반 워크인 100%</b> 달성.</li>
            <li><b>HR 초단기효율화:</b> 점주는 매대에서 탈출해 B2B 단체 정기구독(케이터링) 영업에 사활을 걸고, 매장은 시급 1.3배를 받는 <b>'대기업 매니저급 에이스' 1명</b>이 무결점 통제한다.</li>
        </ul>
        <div style="color:#22c55e; font-weight:900; font-size:1.1rem; margin-top:20px;">➔ 월 순수익 1천만 원 이상 고공행진. 투자 회수 1년 컷.</div>
    </div>
    """, unsafe_allow_html=True)

with col_cs2:
    st.markdown("""
    <div style="background:#111113; border:1px solid #f43f5e; border-radius:8px; padding:20px; height:100%;">
        <h4 style="color:#f43f5e; margin-top:0;">💀 밑빠진 독 (워킹푸어) 함정 모델 (하위 10%)</h4>
        <ul style="color:#d4d4d8; font-size:0.95rem; line-height:1.7;">
            <li><b>가오충 CAPEX:</b> 보여주기식 'S급 메인상권' A급 인테리어 평당 450만 원 박고, <b>정부지원 없이 100% 한도 영끌 대출</b> 시작.</li>
            <li><b>역마진 볼륨화:</b> 객단가 2,000원 아이스 아메리카노만 팔면서, 외형 부풀리려고 <b>플랫폼 배달 비중 70%</b>(수수료 35% 이상 증발)에 목숨 건다.</li>
            <li><b>오퍼레이션 붕괴:</b> 스태프 최저시급 후려치다 무단결근(추노) 맞고, <b>점주 본인이 하루 16시간 매대</b> 닦으면서 고객 컴플레인 맞고 멘탈 붕괴.</li>
        </ul>
        <div style="color:#ef4444; font-weight:900; font-size:1.1rem; margin-top:20px;">➔ 오너 실질 시급 3,000원. 대출 이자에 짓눌려 1년 내 강제 파산.</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<br>
<div style="text-align:right; color:#71717a; font-size:0.8rem;">
T-Protocol Execution complete. (현실 부정 금지)
</div>
""", unsafe_allow_html=True)
