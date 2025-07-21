import streamlit as st
import os
from modules.draw_update import load_draws, get_1st_prize
from modules.base_analysis import (
    load_base_from_file,
    save_base_to_file,
    display_base_as_text,
    score_digits
)
from modules.superbase import generate_super_base
from modules.ai_prediction import generate_predictions, ai_tuner
from modules.cross_analysis import cross_pick_analysis
from modules.insights import get_last_result_insight
from modules.visualizer import show_digit_distribution, show_digit_heatmap

# ===================== Konfigurasi UI =====================
st.set_page_config(page_title="Breakcode4D Visual", layout="centered")
st.title("🔮 Breakcode4D Predictor (GD Lotto)")

# ===================== Butang atas =====================
col_btn1, col_btn2 = st.columns([1, 1])

with col_btn1:
    if st.button("📥 Update Draw Terkini"):
        from modules.draw_update import update_draws
        msg = update_draws()
        st.success(msg)
        st.markdown("### 📋 Base Hari Ini (Salin & Tampal)")
        st.code(display_base_as_text('data/base.txt'), language='text')

with col_btn2:
    st.markdown(
        """
        <a href="https://batman11.net/RegisterByReferral.aspx?MemberCode=BB1845" target="_blank">
            <button style="width: 100%; padding: 0.6em; font-size: 16px; background-color: #4CAF50; color: white; border: none; border-radius: 5px;">
                📝 Register Sini Batman 11 dan dapatkan BONUS!!!
            </button>
        </a>
        """,
        unsafe_allow_html=True
    )

# ===================== Papar draw sedia ada =====================
draws = load_draws()

if draws:
    st.info(f"📅 Tarikh terakhir: **{draws[-1]['date']}** | 📊 Jumlah draw: **{len(draws)}**")

    # ============ Tab Layout =============
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📌 Insight Terakhir",
        "🧠 Ramalan AI",
        "🔁 Analisis Cross Pick",
        "🚀 Super Base & Tuner",
        "📈 Visualisasi"
    ])

    with tab1:
        st.subheader("📌 Insight Nombor Terakhir")
        st.markdown(get_last_result_insight(draws))

    with tab2:
        st.subheader("🧠 Ramalan Berdasarkan Super/Base")
        base_digits = load_base_from_file('data/base_super.txt') if os.path.exists('data/base_super.txt') else load_base_from_file('data/base.txt')
        preds = generate_predictions(base_digits)
        for i, pick in enumerate(base_digits):
            st.write(f"Pick {i+1}: {' '.join(pick)}")

        st.markdown("📊 10 Ramalan Terpilih:")
        col1, col2 = st.columns(2)
        for i in range(5):
            col1.text(preds[i])
            col2.text(preds[i+5])

    with tab3:
        if st.button("🔁 Cross Pick Analysis"):
            st.text(cross_pick_analysis(draws))

    with tab4:
        col4a, col4b = st.columns(2)

        with col4a:
            if st.button("🚀 Jana Super Base (30,60,120)"):
                super_base = generate_super_base(draws)
                save_base_to_file(super_base, 'data/base_super.txt')
                st.success("Super Base disimpan ke 'base_super.txt'")
                st.markdown("### 📋 Super Base (Salin & Tampal)")
                st.code(display_base_as_text('data/base_super.txt'), language='text')

        with col4b:
            if st.button("🧪 Tuner AI (Auto Filter)"):
                tuned = ai_tuner(draws)
                for i, pick in enumerate(tuned):
                    st.write(f"Tuned Pick {i+1}: {' '.join(pick)}")

    with tab5:
        st.subheader("📊 Visualisasi Taburan Digit")
        show_digit_distribution(draws)
        st.subheader("🔥 Heatmap Kekerapan Digit")
        show_digit_heatmap(draws)

else:
    st.warning("⚠️ Sila klik '📥 Update Draw Terkini' untuk mula. Tunggu 1-2 Minit.")