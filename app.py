import streamlit as st
import os
from modules import base_analysis, superbase, ai_prediction, draw_update

# ========== Logo dan Tajuk ==========
st.set_page_config(page_title="Breakcode4D Predictor", layout="wide")
st.image("assets/logo.png", width=120)
st.title("🔮 Breakcode4D Predictor")

# ========== Auto Update Data Jika Kosong ==========
draw_file = "data/draws.txt"
if not os.path.exists(draw_file) or os.stat(draw_file).st_size == 0:
    st.warning("🚨 Tiada data draw ditemui. Sistem sedang mengemaskini 30 draw terkini...")
    msg = draw_update.update_draws(file_path=draw_file, max_days_back=30)
    st.success(msg)

# ========== Sidebar Butang ==========
st.sidebar.button("🔄 Update Draw Terkini", on_click=draw_update.update_draws)
st.sidebar.markdown(
    "[📝 Register Sini](https://batman11.net/RegisterByReferral.aspx?MemberCode=BB1845)",
    unsafe_allow_html=True,
)

# ========== Tab Layout ==========
tab1, tab2, tab3, tab4 = st.tabs(["📌 Insight Terkini", "📊 Base Analysis", "🚀 Super Base", "🤖 AI Prediction"])

with tab1:
    base_analysis.display_last_number_insight()

with tab2:
    base_analysis.display_base_analysis()
    base_analysis.display_base_interface()

with tab3:
    superbase.display_superbase()

with tab4:
    ai_prediction.display_ai_prediction()