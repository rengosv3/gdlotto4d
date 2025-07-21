import streamlit as st
from modules import (
    draw_update,
    base_analysis,
    superbase,
    ai_prediction
)

# ========== Konfigurasi App ==========
st.set_page_config(
    page_title="Breakcode4D Predictor",
    page_icon="🎯",
    layout="wide"
)

# ========== Header ==========
col1, col2 = st.columns([3, 1])
with col1:
    st.image("assets/logo.png", width=120)
    st.title("🎯 Breakcode4D Predictor")
with col2:
    st.markdown("### ")
    st.link_button("🔗 Register Sini Batman 11 dan dapatkan BONUS!!!", "https://batman11.net/RegisterByReferral.aspx?MemberCode=BB1845")
    st.write("")
    draw_update.display_draw_update()

st.markdown("---")

# ========== Tabs ==========
tab1, tab2, tab3, tab4 = st.tabs(["📌 Insight Nombor", "📊 Base Analysis", "🚀 Super Base", "🤖 AI Prediction"])

with tab1:
    base_analysis.display_last_number_insight()

with tab2:
    base_analysis.display_base_analysis()

with tab3:
    superbase.display_superbase()

with tab4:
    ai_prediction.display_ai_prediction()