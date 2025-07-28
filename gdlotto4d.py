import streamlit as st
from insight import show_insight_tab
from prediction import show_prediction_tab
from backtest import show_backtest_tab
from digit_rank import show_digit_rank_tab
from draw_list import show_draw_list_tab
from wheelpick import show_wheelpick_tab
from hit_frequency import show_hit_frequency_tab
from last_hit import show_last_hit_tab
from analisis import show_analisis_tab
from semak_fail import show_semak_fail_tab

from draw_scraper import update_draws
from utils import (
    get_draw_countdown_from_last_8pm,
    load_draws,
    load_base_from_file,
    update_base_today  # ← Ditambah
)

# Config utama
st.set_page_config("Breakcode4D Predictor (GD Lotto) V2.0", layout="wide")

# Header utama
st.title("🔮 Breakcode4D Predictor (GD Lotto) V2.0")
st.markdown("Ramalan 4D berdasarkan strategi Break & AI Pattern")

# Sidebar countdown & action
st.sidebar.markdown("### ⏳ Countdown ke 8PM")
cd = get_draw_countdown_from_last_8pm()
st.sidebar.info(f"{cd.seconds//3600:02}:{(cd.seconds//60)%60:02}:{cd.seconds%60:02} jam")

# Update draws & base
col1, col2 = st.columns(2)
with col1:
    if st.button("📥 Update Draw Terkini"):
        msg = update_draws()
        st.success(msg)
        st.markdown("### 📋 Base Hari Ini")
        base_txt = load_base_from_file()
        st.code('\n'.join([' '.join(p) for p in base_txt]) or "Tiada base.", language='text')

    if st.button("🔄 Update Base Hari Ini"):
        update_base_today()
        st.success("✔️ Base hari ini berjaya dikemaskini.")

# Tabs utama
tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10 = st.tabs([
    "📊 Insight", "📈 Ramalan", "🧪 Backtest", "📋 Draw List", "🔃 Wheelpick",
    "📌 Hit Frequency", "📅 Last Hit", "📶 Digit Rank", "🔍 Analisis", "📁 Semak Fail"
])

with tab1: show_insight_tab()
with tab2: show_prediction_tab()
with tab3: show_backtest_tab()
with tab4: show_draw_list_tab()
with tab5: show_wheelpick_tab()
with tab6: show_hit_frequency_tab()
with tab7: show_last_hit_tab()
with tab8: show_digit_rank_tab()
with tab9: show_analisis_tab()
with tab10: show_semak_fail_tab()

# Footer
st.markdown("---")
st.markdown("📝 [Register Sini Batman 11](https://t.me/batman11bet)")
st.markdown("💬 Hubungi Admin: [@rengosv3](https://t.me/rengosv3)")