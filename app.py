import streamlit as st
from modules import draw_update, base_analysis, ai_prediction, superbase
from datetime import datetime

# Logo
st.set_page_config(page_title="Breakcode4D Predictor", layout="wide")
st.image("assets/logo.png", width=200)

st.title("🔮 Breakcode4D Predictor")

# Butang atas
col1, col2 = st.columns([1, 1])
with col1:
    if st.button("🔄 Update Draw Terkini"):
        draw_update.update_draws()
        st.success("Data draw berjaya dikemas kini.")
with col2:
    st.markdown("[📝 Register Sini](https://batman11.net/RegisterByReferral.aspx?MemberCode=BB1845)", unsafe_allow_html=True)

st.markdown("---")

# Tab utama
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📅 Semakan Draw", 
    "📊 Base Analysis", 
    "🧠 AI Prediction", 
    "🌟 Super Base", 
    "🎯 AI Tuner & Cross Pick", 
    "📌 Insight Nombor Terakhir"
])

# Tab 1: Draw
with tab1:
    draw_update.display_latest_draw()

# Tab 2: Base Analysis
with tab2:
    base_analysis.display_base_interface()

# Tab 3: AI Prediction
with tab3:
    ai_prediction.display_ai_predictions()

# Tab 4: Super Base
with tab4:
    superbase.display_super_base()

# Tab 5: AI Tuner & Cross Pick
with tab5:
    ai_prediction.display_tuner_and_cross_pick()

# Tab 6: Insight
with tab6:
    ai_prediction.display_last_result_insight()
