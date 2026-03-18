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
    <h1 style="color:#f87171; margin:0;">💀 T-Protocol 카페 창업 생존 지옥편</h1>
    <p style="color:#fca5a5; margin-top:5px; font-weight:500;">프차 컨설턴트들이 절대 말 안 하는 진상, 기계 고장, 알바 추노 리스크까지 전부 숫자로 때려 박았다. 멘탈 꽉 잡아라.</p>
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
    st.header("1️⃣ 점포 뼈대 세팅")
    loc_sel = st.selectbox("상권 수준 (현실 파악부터)", list(LOCATIONS.keys()), index=2)
    area = st.number_input("매장 평수", 10, 100, 15)
    loc = LOCATIONS[loc_sel]
    
    dep = st.number_input("보증금 (만원)", 0, 100000, int(loc['보증금평당']*area), step=100)
    kwon = st.number_input("바닥/영업 권리금 (만원) - 날릴 확률 농후", 0, 50000, int(loc['권리금평당']*area), step=100)
    rent = st.number_input("월세 (만원) - 비가 오나 눈이 오나 나감", 0, 5000, int(loc['월세평당']*area), step=10)
    
    st.divider()
    st.header("2️⃣ 매출 허상과 실체")
    unit_price = st.number_input("예상 평균 객단가 (원)", 2000, 20000, 6000, step=500)
    material_ratio = st.slider("기본 원가율 (%) + 우유 버리는 건 덤", 15, 60, 35) / 100.0
    delivery_ratio = st.slider("배달 비중 (%) - 할수록 적자", 0, 80, 30) / 100.0
    delivery_fee_ratio = st.slider("배달앱 삥뜯는 수수료 (%)", 10, 50, 30) / 100.0
    
    st.divider()
    st.header("3️⃣ 인간 갈아넣기 & 지옥의 변수")
    work_hrs = 14
    owner_work = st.slider(f"사장 매장 상주시간 (일 기준, 총 {work_hrs}H 중)", 0, 16, 10)
    alba_count = st.slider("동시 근무 알바 수 (피크타임 대비 비율)", 0.5, 4.0, 1.5, step=0.5, help="1.0이면 항상 1명이 매장을 지킴. 2.0이면 알바 2명이서 14시간 내내 풀가동.")
    pt_wage = st.number_input("알바 시급 (원, 주휴+퇴직금리스크 반영)", 9860, 20000, 12500)
    
    st.markdown("🚨 **[숨겨진 현실 리스크 파라미터]**")
    black_consumer = st.slider("진상 손님 (환불/재결제/서비스 요구 비율 %)", 0.0, 10.0, 2.5, step=0.1) / 100.0
    alba_run = st.number_input("알바 추노 손실 (월 / 무단결근 땜빵급여, 구인광고 등 만원)", 0, 100, 15)
    machine_fail = st.number_input("머신 잔고장/정수필터/에어컨 유지보수 (월 만원)", 0, 80, 10)
    
    st.divider()
    st.header("4️⃣ 대출 (빚쟁이 스타트)")
    my_cash = st.number_input("내 쌩돈 (만원)", 0, 200000, 5000, step=1000)
    interest_rate = st.number_input("대출 금리 (%)", 2.0, 15.0, 6.5, step=0.1) / 100.0

# ── 초기비용 ──
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
        <div class="fact-title">🚨 데스 스파이럴(Death Spiral). 구조적 한계 도달 🚨</div>
        <div class="fact-text">매월 <b>{int(abs(net_profit)/10000):,}만 원</b> 규모의 영속적 적자가 발생 중이다. 
        현재의 배달플랫폼 수수료와 인건비 포화 상태로는 사장이 노동력을 극단적으로 투입해도 회복이 불가능하다. 
        대출 회전율 상승이나 권리금 회수 같은 막연한 희망회로를 차단하고 당장 손절매(Loss Cut) 결단이 요구된다.<br><br>
        <span style="color:#34d399;"><b>🌱 [T-Protocol 비상 대책]</b> 단, 매몰비용에 갇혀 완전히 이성을 잃지 않았다면 최하단의 '생존 처방전'을 기반으로 즉각적인 고강도 체질 개선과 영업방식 재편을 밀어붙여라. 숫자는 거짓말을 하지 않는다.</span></div>
    </div>""", unsafe_allow_html=True)
elif owner_hourly_wage < pt_wage:
    st.markdown(f"""<div class="fact-box" style="border-color:#fbbf24;">
        <div class="fact-title">⚠️ 워킹푸어형 좀비 기업. 실질 기회비용 마이너스 ⚠️</div>
        <div class="fact-text">월 <b>{owner_monthly_hours}시간</b>의 오너 노동력을 투입하고도 확보한 순수익은 <b>{int(net_profit/10000):,}만 원</b>에 불과하다. 
        최종 실질 수익 파이프라인 대비 시급이 <b>{int(owner_hourly_wage):,}원</b>으로 일반 파트타이머(기본급 {pt_wage}원)보다 못한 최악의 자영업 함정에 빠졌다. 
        비즈니스 시스템이 아닌 점주의 육체노동 점거율에 단일 의존하는 전형적인 '자기 고용 노예' 상태다. 즉시 구조 개선이 시급하다.</div>
    </div>""", unsafe_allow_html=True)
else:
    months_to_rec = (total_startup * 10000) / net_profit
    if net_profit >= 10000000 or months_to_rec <= 24:
        st.markdown(f"""<div class="fact-box" style="border-color:#3b82f6;">
            <div class="fact-title">📈 최상위 캐시카우. 압도적 현금창출력 확보 📈</div>
            <div class="fact-text">월 순수익 <b>{int(net_profit/10000):,}만 원</b>, 오너 실질 시급 <b>{int(owner_hourly_wage):,}원</b>. 투자 대비 수익률(ROI) 최상위 구간에 완벽하게 안착했다. 
            CS 컴플레인 리스크(월 <b>{int(black_consumer_loss/10000):,}만 원</b> 손실)와 영업상 통상 감가상각을 모두 맞고도 
            초기 총투입 자본금 <b>{total_startup:,}만 원</b> 전액 회수에 고작 <b>{months_to_rec/12:.1f}년 ({int(months_to_rec)}개월)</b>이 소요된다. 현재의 비즈니스 해자를 기반으로 스케일업(다점포 전개 및 법인화)을 최우선 검토해라.</div>
        </div>""", unsafe_allow_html=True)
    else:
        st.markdown(f"""<div class="fact-box" style="border-color:#4ade80;">
            <div class="fact-title">✅ 영업 흑자 달성. 자본 회수(ROI) 진행 중 ✅</div>
            <div class="fact-text">월 순수익 <b>{int(net_profit/10000):,}만 원</b>으로 운영수익 흑자 방어선을 뚫어냈다. 
            그러나 악성고객 방어 한계(추정액 <b>{int(black_consumer_loss/10000):,}만 원</b>) 및 HR/설비 돌발 변수(월 <b>{(alba_run+machine_fail):,}만 원</b>) 등 리퀴디티(유동성) 타격 팩터가 잔존한다. 
            현 런레이트 기준 전액 투자금 <b>{total_startup:,}만 원</b> 회수까지 <b>{months_to_rec/12:.1f}년 ({int(months_to_rec)}개월)</b>이 추산된다. 경제 불황이나 동종업 진입에 대비해 잉여 유보금(Cash Reserve) 조기 편성에 집중해라.</div>
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
        "text": "매출의 15% 이상이 고정 임대료로 소진되고 있다. 오프라인 회전율 한계를 배달/포장의 타겟팅 변경 투입으로 상쇄하거나, 수익성 중심의 B급 상권으로 즉각 상가 다운사이징(Downsizing)을 추진해라."
    },
    {
        "trigger": material_ratio > 0.35,
        "title": f"원부자재 코스트 과부하 (COGS: 현재 {material_ratio*100:.1f}%)",
        "text": "프랜차이즈 종속 또는 자체 레시피 과소비로 마진이 붕괴됐다. 객단가 인상 및 마진율 최적화율 70% 이상인 하이엔드/저단가 디저트류 결합 프로모션 전개를 통한 판매단가 재조립(Re-pricing) 로직이 도입되어야 한다."
    },
    {
        "trigger": delivery_ratio >= 0.30 and delivery_fee_ratio >= 0.20,
        "title": f"배달 채널 수익잠식 (Platform Dependency: 플랫폼 종속비용 {delivery_fee_ratio*100:.1f}%)",
        "text": "매출 외형만 팽창하고 실질 영업이익은 딜리버리 수수료 명목하에 전액 흡수당하고 있다. 자사 멤버십(LTV) 프로모션 강화를 통해 워크인(Walk-in) 및 매장형 방문객 포지션을 강제로 70% 대역까지 끌어올리는 채널 자립 락인(Lock-in) 전략을 당장 시현해라."
    },
    {
        "trigger": hidden_risk_cost > 500000,
        "title": f"운영/CS 리스크 관리 실패 (HR & CS Loss: 손실 누적액 최고 월 {int(hidden_risk_cost/10000)}만 도달)",
        "text": "인력 교체에 따른 채용 및 OJT(교육) 매몰비용과 블랙컨슈머발 재화 소진율이 극위험 수위다. 코어 인력(Core HR)에게 근속 리텐션 보너스를 부여해 근본 이탈 원인을 통제하는 것이 잦은 이탈로 발생할 복수의 기회비용 소모를 끊어내는 가장 효율적인 레버리지다."
    },
    {
        "trigger": owner_hourly_wage < pt_wage,
        "title": f"기회비용 상실형 구조 (Low ROI on Owner's Time: 실질 시급 단가 {int(owner_hourly_wage)}원)",
        "text": f"오너 내부 노동 투입({owner_monthly_hours}시간) 대비 산출 가치가 시장 하한선(최저시준액 {pt_wage}원) 미만이다. 로컬 매대 방어를 스태프에게 전면 이관하고, 오너는 B2B 대량 납품 수주(인근 공단 제휴 등) 및 광역 마케팅 등 고부가가치 아웃바운드 업무 파이프라인 개설에 사활을 걸어라."
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
