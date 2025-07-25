import streamlit as st
import pandas as pd

from utils import (
    get_draw_countdown_from_last_8pm,
    load_draws,
    load_base_from_file
)
from draw_scraper import update_draws
from strategies import generate_base
from prediction import generate_predictions_from_base
from backtest import run_backtest
from wheelpick import (
    get_like_dislike_digits,
    generate_wheel_combos,
    filter_wheel_combos
)
from hit_frequency import show_hit_frequency_tab
from last_hit import show_last_hit_tab
from combined_insight import show_combined_insight_tab

st.set_page_config(page_title="Breakcode4D Predictor", layout="wide")
st.title("🔮 Breakcode4D Predictor (GD Lotto) V2.0")
st.markdown(f"⏳ Next draw in: `{str(get_draw_countdown_from_last_8pm()).split('.')[0]}`")

# Update draws & base
col1, col2 = st.columns(2)
with col1:
    if st.button("📥 Update Draw Terkini"):
        msg = update_draws()
        st.success(msg)
        st.markdown("### 📋 Base Hari Ini")
        base_txt = load_base_from_file()
        st.code('\n'.join([' '.join(p) for p in base_txt]) or "Tiada base.", language='text')
with col2:
    st.markdown("""
    <a href="https://batman11.net/RegisterByReferral.aspx?MemberCode=BB1845" target="_blank">
      <button style="width:100%;padding:0.6em;font-size:16px;background:#4CAF50;color:white;border:none;border-radius:5px;">
        📝 Register Sini Batman 11 dan dapatkan BONUS!!!
      </button>
    </a>
    """, unsafe_allow_html=True)

# Load draws
draws = load_draws()
if not draws:
    st.warning("⚠️ Sila klik 'Update Draw Terkini' untuk mula.")
    st.stop()

st.info(f"📅 Tarikh terakhir: **{draws[-1]['date']}** | 📊 Jumlah draw: **{len(draws)}**")

tabs = st.tabs([
    "Insight",
    "Ramalan",
    "Backtest",
    "Draw List",
    "Wheelpick",
    "Hit Frequency",
    "Last Hit"
])

# Tab 1: Insight
with tabs[0]:
    st.header("📌 Insight Terakhir")
    last = draws[-1]
    try:
        base_last = load_base_from_file('data/base_last.txt')
    except:
        base_last = []
    if not base_last:
        st.warning("⚠️ Base terakhir belum wujud. Update dulu.")
    else:
        st.markdown(f"**Tarikh Draw:** `{last['date']}`  \n**1st Prize:** `{last['number']}`")
        cols = st.columns(4)
        for i in range(4):
            dig = last['number'][i]
            if dig in base_last[i]:
                cols[i].success(f"P{i+1}: ✅ `{dig}`")
            else:
                cols[i].error(f"P{i+1}: ❌ `{dig}`")

        st.markdown("---")
        st.subheader("Perbandingan Strategi")
        arah = st.radio("Arah Digit:", ["Kiri→Kanan", "Kanan→Kiri"], key="insight_dir")
        recent_n = st.slider("Draw untuk base:", 10, len(draws), 50, 5, key="insight_n")

        strategies = ['frequency', 'gap', 'hybrid', 'qaisara', 'smartpattern', 'hitfq']
        rows = []
        for strat in strategies:
            try:
                base = generate_base(draws[:-1], method=strat, recent_n=recent_n)
                if arah == "Kanan→Kiri":
                    fp = last['number'][::-1]
                else:
                    fp = last['number']
                flags = ["✅" if fp[i] in base[i] else "❌" for i in range(4)]
                rows.append({
                    "Strategi": strat,
                    "P1": flags[0], "P2": flags[1],
                    "P3": flags[2], "P4": flags[3],
                    "✅ Total": flags.count("✅")
                })
            except Exception:
                pass

        if rows:
            df_insight = pd.DataFrame(rows).sort_values("✅ Total", ascending=False)
            st.dataframe(df_insight, use_container_width=True)
        else:
            st.warning("❗ Tidak cukup data untuk perbandingan.")

# Tab 2: Ramalan
with tabs[1]:
    st.header("🧠 Ramalan Base")
    strategies = ['frequency', 'gap', 'hybrid', 'qaisara', 'smartpattern', 'hitfq']
    strat = st.selectbox("Strategi:", strategies, key="pred_strat")
    recent_n2 = st.slider("Draw terkini:", 5, len(draws), 30, 5, key="pred_n")

    try:
        base = generate_base(draws, method=strat, recent_n=recent_n2)
        for i, p in enumerate(base, start=1):
            st.text(f"P{i}: {' '.join(p)}")
        preds = generate_predictions_from_base(base, max_preds=10)
        st.markdown("**🔢 Top 10 Ramalan:**")
        st.code('\n'.join(preds), language='text')
    except Exception as e:
        st.error(str(e))

# Tab 3: Backtest
with tabs[2]:
    st.header("🔁 Backtest Base")
    arah_bt = st.radio("Arah:", ["Kiri→Kanan", "Kanan→Kiri"], key="bt_dir")
    strategies = ['frequency', 'gap', 'hybrid', 'qaisara', 'smartpattern', 'hitfq']
    strat_bt = st.selectbox("Strategi:", strategies, key="bt_strat")
    n_bt = st.slider("Draw untuk base:", 5, len(draws), 30, 5, key="bt_n")
    rounds = st.slider("Bilangan backtest:", 5, 50, 10, key="bt_rounds")

    if st.button("🚀 Jalankan Backtest", key="bt_run"):
        try:
            df_bt, matched = run_backtest(
                draws,
                strategy=strat_bt,
                recent_n=n_bt,
                arah='right' if arah_bt == "Kanan→Kiri" else 'left',
                backtest_rounds=rounds
            )
            st.success(f"🎯 Matched: {matched} daripada {rounds}")
            st.dataframe(df_bt, use_container_width=True)
        except Exception as e:
            st.error(str(e))

# Tab 4: Draw List
with tabs[3]:
    st.header("📋 Senarai Draw")
    st.dataframe(pd.DataFrame(draws), use_container_width=True)

# Tab 5: Wheelpick
with tabs[4]:
    st.header("🎡 Wheelpick Generator")
    arah_wp = st.radio("Arah:", ["Kiri→Kanan", "Kanan→Kiri"], key="wp_dir")
    like, dislike = get_like_dislike_digits(draws)
    st.markdown(f"👍 Like: `{like}`    👎 Dislike: `{dislike}`")
    user_like = st.text_input("Digit Like:", value=' '.join(like), key="wp_like")
    user_dislike = st.text_input("Digit Dislike:", value=' '.join(dislike), key="wp_dislike")
    likes = user_like.split()
    dislikes = user_dislike.split()

    # Manual vs Auto toggle
    input_mode = st.radio("Input Base:", ["Auto dari strategi", "Manual"], key="wp_mode")

    if input_mode == "Auto dari strategi":
        strategies = ['frequency', 'gap', 'hybrid', 'qaisara', 'smartpattern', 'hitfq']
        strat_wp = st.selectbox("Strategi Base:", strategies, key="wp_strat")
        recent_wp = st.slider("Draw untuk base:", 5, len(draws), 30, 5, key="wp_n")
        try:
            base_wp = generate_base(draws, method=strat_wp, recent_n=recent_wp)
        except Exception as e:
            st.error(str(e))
            st.stop()
    else:
        manual_base = st.text_area("Masukkan Base Manual (4 baris, digit pisah space)", height=120, key="wp_manual")
        try:
            base_wp = [line.strip().split() for line in manual_base.strip().split('\n')]
            if len(base_wp) != 4 or any(not p for p in base_wp):
                raise ValueError("Format base tak sah.")
        except Exception as e:
            st.error(f"Base manual error: {str(e)}")
            st.stop()

    lot = st.text_input("Nilai Lot:", value="0.10", key="wp_lot")

    with st.expander("⚙️ Tapisan Tambahan"):
        no_repeat = st.checkbox("Buang digit ulang", key="f1")
        no_triple = st.checkbox("Buang triple", key="f2")
        no_pair = st.checkbox("Buang pair", key="f3")
        no_ascend = st.checkbox("Buang menaik", key="f4")
        use_history = st.checkbox("Buang pernah keluar", key="f5")
        sim_limit = st.slider("Max sama dgn last draw:", 0, 4, 2, key="f6")

    if st.button("🎰 Create Wheelpick", key="wp_run"):
        arah = "kiri" if arah_wp == "Kiri→Kanan" else "kanan"
        combos = generate_wheel_combos(base_wp, lot=lot, arah=arah)
        st.info(f"Sebelum tapis: {len(combos)}")
        filtered = filter_wheel_combos(
            combos, draws,
            no_repeat, no_triple, no_pair, no_ascend,
            use_history, sim_limit,
            likes, dislikes
        )
        st.success(f"Selepas tapis: {len(filtered)}")
        for i in range(0, len(filtered), 30):
            part = filtered[i:i+30]
            st.markdown(f"**Bahagian {(i//30)+1}:**")
            st.code('\n'.join(part), language='text')
        data = '\n'.join(filtered).encode()
        st.download_button("💾 Muat Turun", data=data,
                           file_name="wheelpick.txt", mime="text/plain")

# Tab 6: Hit Frequency
with tabs[5]:
    show_hit_frequency_tab(draws)

# Tab 7: Last Hit
with tabs[6]:
    show_last_hit_tab(draws)
    
# Dalam `tabs[5]` atau mana-mana:
with tabs[5]:
    show_combined_insight_tab(draws)