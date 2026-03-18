import streamlit as st

st.title("Streamlit 예시 페이지")
st.header("이건 Header 입니다")
st.subheader("이건 Subheader 입니다")

st.text("단순한 텍스트입니다.")
st.caption("이건 캡션(작은 글씨)입니다.")

st.markdown("**마크다운** 문법도 _사용_ 가능")


import pandas as pd

st.title("st.write() 예시")

st.write("이건 문자열 출력입니다.")
st.write("**마크다운 문법**도 자동 인식됩니다.")

st.write("계산 예시:", 10 + 5)
st.write("LaTeX 수식 예시:", r"$a^2 + b^2 = c^2$")

df = pd.DataFrame({
    "이름": ["A", "B", "C"],
    "점수": [85, 90, 78]
})
st.write("데이터프레임 예시:", df)


import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# 예시 데이터
x = np.linspace(0, 10, 50)
y1 = np.sin(x)
y2 = np.cos(x)

fig1, ax1 = plt.subplots()
ax1.plot(x, y1, label='sin(x)')
ax1.plot(x, y2, label='cos(x)')
ax1.legend()
st.pyplot(fig1)

fig2, ax2 = plt.subplots()
ax2.bar(["A", "B", "C"], [10, 25, 15])
st.pyplot(fig2)

fig3, ax3 = plt.subplots()
ax3.scatter(x, y1, color='red')
st.pyplot(fig3)


import plotly.express as px
import streamlit as st
import pandas as pd

df = pd.DataFrame({
    "nation": ["한국", "미국", "일본", "중국", "독일"],
    "gold": [29, 19, 27, 18, 5],
    "silver": [3, 41, 14, 32, 11],
    "bronze": [9, 33, 17, 18, 16]
})

fig = px.pie(df, names='nation', values='gold',
             title='올림픽 양궁 금메달 현황', hole=.3)
st.plotly_chart(fig)
