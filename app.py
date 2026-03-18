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
    page_title="💀 카페 창업 생존 시뮬레이터: 극현실 지옥편",
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
.fact-box { border-left: 4px solid #ef4444; background: #27272a; padding: 15px; margin: 15px 0; border-radius: 0 8px 8px 0; }
.fact-title { color: #ef4444; font-weight: 900; font-size: 1.1rem; margin-bottom: 5px; }
.fact-text { color: #d4d4d8; font-size: 0.95rem; line-height: 1.5; }
.header-tprot { background: linear-gradient(90deg, #7f1d1d, #450a0a); padding: 20px; border-radius: 10px; border-left: 5px solid #f87171; margin-bottom: 20px; }
h3 { margin-top: 1.5rem; }
.stSlider > div > div > div > div { background-color: #ef4444; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="header-tprot">
    <h1 style="color:#f87171; margin:0;">💀 T-Protocol: 저가커피 프랜차이즈 창업 실전 재무 진단기</h1>
    <p style="color:#fca5a5; margin-top:5px; font-weight:500;">프랜차이즈 본사 영업사원은 절대 말해주지 않는 가맹점 실질 수익률(Margin)과 단위경제학(Unit Economics) 팩트 체크.</p>
</div>
""", unsafe_allow_html=True)

# ── 데이터셋 ──
LOCATIONS = {
    "S급 (메인상권)": {"보증금평당": 350, "월세평당": 25, "권리금평당": 400, "회전율": 6.0, "인테리어": 450},
    "A급 (번화가)": {"보증금평당": 250, "월세평당": 15, "권리금평당": 200, "회전율": 4.5, "인테리어": 350},
    "B급 (오피스/대학가)": {"보증금평당": 150, "월세평당": 10, "권리금평당": 100, "회전율": 3.0, "인테리어": 280},
    "C급 (동네 구석)": {"보증금평당": 100, "월세평당": 6, "권리금평당": 20, "회전율": 1.5, "인테리어": 200},
}

with st.sidebar:
    st.header("1️⃣ 입지 및 투자비용 (CAPEX)")
    loc_sel = st.selectbox("상권 수준 (현실 파악부터)", list(LOCATIONS.keys()), index=2)
    area = st.number_input("매장 평수", 10, 100, 15)
    loc = LOCATIONS[loc_sel]
    
    dep = st.number_input("보증금 (만원)", 0, 100000, int(loc['보증금평당']*area), step=100)
    kwon = st.number_input("바닥/영업 권리금 (만원) - 날릴 확률 농후", 0, 50000, int(loc['권리금평당']*area), step=100)
    rent = st.number_input("월세 (만원) - 비가 오나 눈이 오나 나감", 0, 5000, int(loc['월세평당']*area), step=10)
    
    st.divider()
    st.header("2️⃣ 매출 볼륨 및 원가 구조 (COGS)")
    unit_price = st.number_input("예상 평균 객단가 (원)", 2000, 20000, 5000, step=500, help="저가커피는 아메리카노 1500~2000원이지만, 디저트/에이드 묶어파는 평균 객단가를 입력해라.")
    material_ratio = st.slider("원부자재 원가율 (%) - 본사 필수물대 포함", 15, 60, 35) / 100.0
    delivery_ratio = st.slider("배달 비중 (%) - 할수록 역마진 직행", 0, 80, 20) / 100.0
    delivery_fee_ratio = st.slider("배달 플랫폼 수수료 및 부대비용 (%)", 10, 50, 25) / 100.0
    
    st.divider()
    st.header("3️⃣ 오퍼레이션 및 리스크 제어")
    work_hrs = 14
    owner_work = st.slider(f"가맹점주 상주시간 (일 기준, 총 {work_hrs}H 중)", 0, 16, 10)
    alba_count = st.slider("동시 근무 매니저/스태프 수 비율", 0.5, 4.0, 1.5, step=0.5, help="피크타임 샷 뽑는 노동 강도 고려. 메가급은 피크 때 3-4명도 갈아넣는다.")
    pt_wage = st.number_input("스태프 실질 시급 (주휴+퇴직금리스크 반영)", 9860, 20000, 12500)
    
    st.markdown("🚨 **[운영 리스크 파라미터 (HR/CS/설비)]**")
    black_consumer = st.slider("강성 클레임 & 서비스 환불 손실률 (%)", 0.0, 10.0, 2.5, step=0.1) / 100.0
    alba_run = st.number_input("인력 이탈 OJT 매몰비용 (구인/교육/결근 월 만원)", 0, 100, 15)
    machine_fail = st.number_input("에스프레소 머신/제빙기 등 설비 감가상각 (월 만원)", 0, 80, 15)
    
    st.divider()
    st.header("4️⃣ 자본 레버리지 (금융 비용)")
    my_cash = st.number_input("자기 자본 (만원)", 0, 200000, 5000, step=1000)
    interest_rate = st.number_input("대출 금리 (%)", 2.0, 15.0, 6.5, step=0.1) / 100.0

# ── 초기투자 (CAPEX) ──
int_cost = loc['인테리어'] * area
machine_cost = 2500 
etc_start_cost = 1000 
total_startup = dep + kwon + int_cost + machine_cost + etc_start_cost
loan_amt = max(0, total_startup - my_cash)

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
monthly_labor = alba_hours * pt_wage * 30

# 고정 & 현실 반영 변동비
monthly_interest = loan_amt * interest_rate / 12 * 10000
utility = area * 60000 
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
    months_to_rec = (total_startup * 10000) / net_profit
    if net_profit >= 10000000 or months_to_rec <= 24:
        st.markdown(f"""<div class="fact-box" style="border-color:#3b82f6;">
            <div class="fact-title">📈 엑설런트 박리다매! 압도적 볼륨(Volume) 강점 확보 📈</div>
            <div class="fact-text">저가형 프랜차이즈의 로망인 '터지는 회전율'을 달성했다. 월 순수익 <b>{int(net_profit/10000):,}만 원</b>에 투자금 <b>{total_startup:,}만 원</b> 회수율 <b>{months_to_rec/12:.1f}년 ({int(months_to_rec)}개월)</b>이라는 메가급 초고속 캐시카우를 구축했다. 
            진상 고객 한두 명(월 <b>{int(black_consumer_loss/10000):,}만 원</b> 손실)이나 알바 교체비용 정도는 거뜬히 씹어먹는 규모의 경제를 입증했다. 
            현재 시스템과 인적 자원을 고도화시켜 인근 상권에 2호점 출점(다점포 전개)을 준비하는 등 자본 스케일업을 도모해라!</div>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""<div class="fact-box" style="border-color:#4ade80;">
            <div class="fact-title">✅ 영업이익권 진입 완료. 운영 최적화(Optimization) 방어전 돌입 ✅</div>
            <div class="fact-text">치열한 마진 싸움 끝에 <b>{int(net_profit/10000):,}만 원</b>의 영업 흑자 방어선을 뚫어냈다. 
            그러나 박리다매 구조에서 가장 무서운 건 슬로우 시즌 타격이나 예기치 못한 제빙기 고장(월 <b>{(alba_run+machine_fail):,}만 원</b> 소요) 같은 유동성 변수다. 
            현재 수익 흐름 기준 초기 자본금 <b>{total_startup:,}만 원</b> 완전 회수까지 <b>{months_to_rec/12:.1f}년 ({int(months_to_rec)}개월)</b>이 예상된다. 경쟁 저가 커피 브랜드 기습 입점에 대비해 내부 사내유보금을 즉시 쌓아라.</div>
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

st.markdown("""
<br>
<div style="text-align:right; color:#71717a; font-size:0.8rem;">
T-Protocol Execution complete. (현실 부정 금지)
</div>
""", unsafe_allow_html=True)
