import streamlit as st
import os
import inspect

from modules import base_analysis, draw_update, superbase

st.set_page_config(page_title="Breakcode4D Predictor", layout="wide")
st.title("🔮 Breakcode4D Predictor")

# Papar path fail untuk debug (pilihan)
st.caption(f"📁 base_analysis loaded from: {inspect.getfile(base_analysis)}")
st.caption(f"📁 draw_update loaded from: {inspect.getfile(draw_update)}")
st.caption(f"📁 superbase loaded from: {inspect.getfile(superbase)}")

# Butang Update dan Register
colA, colB = st.columns([2, 2])
with colA:
    draw_update.display_draw_update()
with colB:
    st.markdown("### 📌 Register Breakcode4D")
    st.link_button("📝 Register Sini", "https://batman11.net/RegisterByReferral.aspx?MemberCode=BB1845")

# Layout Tab
tabs = st.tabs(["📊 Base Digit", "📈 Analisis", "📌 Nombor Terakhir", "🤖 AI Prediction", "🌟 Super Base"])

with tabs[0]:
    base_analysis.display_base_interface()

with tabs[1]:
    base_analysis.display_base_analysis()

with tabs[2]:
    base_analysis.display_last_number_insight()

with tabs[3]:
    from modules.base_analysis import display_ai_prediction
    display_ai_prediction()

with tabs[4]:
    superbase.display_super_base()