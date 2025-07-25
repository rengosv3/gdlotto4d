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

    digits = list(input_number)
    st.markdown("**📌 Posisi Digit:**")
    cols = st.columns(4)
    for i in range(4):
        cols[i].markdown(f"**P{i+1}:** `{digits[i]}`")

    # Statistik
    st.markdown("---")
    st.subheader("📊 Statistik Digit")

    last_hits = get_last_hit(draws)
    freqs = get_frequency(draws)

    data = []
    for i, d in enumerate(digits):
        freq = freqs[d]
        last_hit = last_hits[d] if d in last_hits else "N/A"
        status = "🔥 Hot" if freq >= 10 else "🧊 Cool"
        data.append({
            "Posisi": f"P{i+1}",
            "Digit": d,
            "Kekerapan": freq,
            "Last Hit": last_hit,
            "Status": status
        })

    st.dataframe(pd.DataFrame(data), use_container_width=True)

    # Semakan Strategi
    st.markdown("---")
    st.subheader("✅ Semakan Dalam Base Strategi")

    rows = []
    for strat in strategies:
        try:
            base = generate_base(draws, method=strat, recent_n=30)
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

    df_check = pd.DataFrame(rows)
    df_check = df_check.sort_values("✅ Total", ascending=False)

    # Skor & Strategi terbaik
    top_row = df_check.iloc[0]
    best_strat = top_row["Strategi"]
    total_match = top_row["✅ Total"]

    st.success(f"🎯 Strategi terbaik: `{best_strat}` dengan `{total_match}/4` padanan digit.")
    st.markdown(f"### ⭐ Skor Keseluruhan: `{total_match}/4`")

    st.dataframe(df_check, use_container_width=True)


def get_last_hit(draws):
    last_seen = {}
    for i in range(len(draws)-1, -1, -1):
        num = draws[i]["number"]
        for d in num:
            if d not in last_seen:
                last_seen[d] = len(draws) - i
    return last_seen


def get_frequency(draws):
    all_digits = ''.join(d["number"] for d in draws)
    return Counter(all_digits)