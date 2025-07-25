import streamlit as st
import pandas as pd
from collections import Counter
from strategies import generate_base

strategies = ['frequency', 'gap', 'hybrid', 'break', 'smartpattern', 'hitfq']

def show_analisis_tab(draws):
    st.header("🔍 Analisis Nombor 4D")

    input_number = st.text_input("Masukkan Nombor 4D:", value="1234", max_chars=4, key="anlz_input")
    if len(input_number) != 4 or not input_number.isdigit():
        st.warning("⚠️ Sila masukkan nombor 4 digit yang sah.")
        return

    # Pilihan sliding window draw
    recent_n = st.slider("Jumlah draw terkini untuk analisis:", 10, len(draws), min(60, len(draws)), 5, key="anlz_recent")
    recent_draws = draws[-recent_n:]

    # Pecahan posisi
    digits = list(input_number)
    st.markdown("**📌 Posisi Digit:**")
    cols = st.columns(4)
    for i, d in enumerate(digits):
        cols[i].markdown(f"**P{i+1}:** `{d}`")

    # Statistik per posisi
    st.markdown("---")
    st.subheader(f"📊 Statistik Digit (Last {recent_n} Draw)")
    last_hits = _get_last_hit(recent_draws)
    freqs = _get_frequency(recent_draws)

    stats = []
    for i, d in enumerate(digits):
        freq = freqs[i].get(d, 0)
        last_hit = last_hits.get(d, "N/A")
        status = "🔥 Hot" if freq >= (recent_n * 0.2) else "🧊 Cool"
        stats.append({
            "Posisi": f"P{i+1}",
            "Digit": d,
            "Kekerapan": freq,
            "Last Hit": last_hit,
            "Status": status
        })
    st.dataframe(pd.DataFrame(stats), use_container_width=True)

    # Semakan strategi
    st.markdown("---")
    st.subheader("✅ Semakan Dalam Base Strategi")
    rows = []
    for strat in strategies:
        try:
            base = generate_base(recent_draws, method=strat, recent_n=recent_n)
            flags = ["✅" if digits[i] in base[i] else "❌" for i in range(4)]
            rows.append({
                "Strategi": strat,
                "P1": flags[0], "P2": flags[1],
                "P3": flags[2], "P4": flags[3],
                "✅ Total": flags.count("✅")
            })
        except Exception:
            continue

    if not rows:
        st.warning("❗ Tiada strategi dapat dianalisis.")
        return

    df = pd.DataFrame(rows).sort_values("✅ Total", ascending=False)
    best = df.iloc[0]
    st.success(f"🎯 Strategi terbaik: `{best['Strategi']}` dengan `{best['✅ Total']}/4` padanan digit.")
    st.markdown(f"### ⭐ Skor Keseluruhan: `{best['✅ Total']}/4`")
    st.dataframe(df, use_container_width=True)


def _get_last_hit(draws):
    """Kira draw ke berapa terakhir setiap digit muncul (global, bukan ikut posisi)"""
    last_seen = {}
    for i, draw in enumerate(draws[::-1]):  # draw terbaru ke lama
        for d in draw["number"]:
            if d not in last_seen:
                last_seen[d] = i + 1
    return last_seen


def _get_frequency(draws):
    """Kira kekerapan setiap digit ikut posisi"""
    pos_freq = [Counter() for _ in range(4)]
    for draw in draws:
        number = draw["number"]
        for i in range(4):
            pos_freq[i][number[i]] += 1
    return pos_freq