import streamlit as st
import os
import inspect
from modules import base_analysis, superbase, ai_prediction, draw_update

# ========== Konfigurasi Awal ==========
st.set_page_config(page_title="Breakcode4D Predictor", layout="wide")

# ========== Debug (Opsyenal) ==========
# st.write("📁 base_analysis path:", inspect.getfile(base_analysis))
# st.write("📦 Functions in base_analysis:", dir(base_analysis))

# ========== Fungsi Auto Update Jika Fail Kosong ==========
def auto_update_if_empty():
    draw_file = "data/draws.txt"
    if not os.path.exists(draw_file) or os.stat(draw_file).st_size == 0:
        st.warning("🚨 Tiada data draw ditemui. Klik 'Update Draw Terkini' untuk mula.")
        return False
    return True

# ========== Logo & Tajuk ==========
st.image("assets/logo.png", width=120)
st.title("🔮 Breakcode4D Predictor")

# ========== Sidebar ==========
with st.sidebar:
    if st.button("🔄 Update Draw Terkini"):
        msg = draw_update.update_draws(file_path="data/draws.txt", max_days_back=30)
        st.success(msg)

    st.markdown(
        "[📝 Register Sini](https://batman11.net/RegisterByReferral.aspx?MemberCode=BB1845)",
        unsafe_allow_html=True,
    )

# ========== Kandungan Utama ==========
if auto_update_if_empty():
    tab1, tab2, tab3, tab4 = st.tabs([
        "📌 Insight Terkini",
        "📊 Base Analysis",
        "🚀 Super Base",
        "🤖 AI Prediction"
    ])

    with tab1:
        base_analysis.display_last_number_insight()

    with tab2:
        base_analysis.display_base_analysis()
        base_analysis.display_base_interface()

    with tab3:
        superbase.display_superbase()

    with tab4:
        ai_prediction.display_ai_prediction()
else:
    st.info("Sila tekan butang 'Update Draw Terkini' di sidebar untuk mula.")