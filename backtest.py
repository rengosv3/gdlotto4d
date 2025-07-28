import streamlit as st
import pandas as pd

from utils import load_draws
from strategies import generate_base
from backtest import run_backtest, evaluate_strategies

strategies_available = ['frequency', 'polarity_shift', 'hybrid', 'break', 'smartpattern', 'hitfq']

def show_backtest_tab():
    st.subheader("🔁 Backtest Strategi")

    draws = load_draws()
    if len(draws) < 100:
        st.warning("Data draw belum cukup. Minimum 100 draw diperlukan untuk backtest.")
        return

    col1, col2 = st.columns(2)
    with col1:
        strategy = st.selectbox("Pilih Strategi", strategies_available, index=2)
        arah = st.selectbox("Arah", ['left', 'right'], index=0)
    with col2:
        recent_n = st.slider("Bilangan Draw Terkini", 30, 100, 50, step=5)
        bt_rounds = st.slider("Bilangan Ujian (round)", 5, 30, 10, step=1)

    if st.button("Run Backtest"):
        try:
            df, matched = run_backtest(draws, strategy=strategy, recent_n=recent_n, arah=arah, backtest_rounds=bt_rounds)
            st.success(f"Jumlah draw dengan 4 digit padanan penuh: {matched} / {bt_rounds}")
            st.dataframe(df, use_container_width=True)
        except Exception as e:
            st.error(f"Ralat: {e}")

    with st.expander("📊 Penilaian Semua Strategi"):
        eval_df = evaluate_strategies(draws)
        st.dataframe(eval_df, use_container_width=True)