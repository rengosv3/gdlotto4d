import streamlit as st
from insight import show_insight_tab
from prediction import show_prediction_tab
from backtest import show_backtest_tab
from digit_rank import show_digit_rank_tab
from draw_list import show_draw_list_tab
from analisis import show_analisis_tab
from checkfile import show_checkfile_tab
from utils import update_draws, update_base_today

st.set_page_config(page_title="GDLOTTO4D", layout="wide")
st.title("🎯 GDLOTTO 4D SYSTEM V2.0")

# Sidebar: Update draw dan base
st.sidebar.header("Kemaskini Data")
if st.sidebar.button("Update Draw Hari Ini"):
    update_draws(1)
    st.sidebar.success("✔️ Draw hari ini berjaya dikemaskini.")
if st.sidebar.button("Update Base Hari Ini"):
    update_base_today()
    st.sidebar.success("✔️ Base hari ini berjaya dikemaskini.")

# Tab utama
tabs = st.tabs(["Insight", "Ramalan", "Backtest", "Digit Rank", "Senarai Draw", "Analisis", "Semak Fail"])
with tabs[0]: show_insight_tab()
with tabs[1]: show_prediction_tab()
with tabs[2]: show_backtest_tab()
with tabs[3]: show_digit_rank_tab()
with tabs[4]: show_draw_list_tab()
with tabs[5]: show_analisis_tab()
with tabs[6]: show_checkfile_tab()