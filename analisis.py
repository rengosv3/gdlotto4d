import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
from strategies import generate_base

strategies = ['frequency', 'gap', 'hybrid', 'break', 'smartpattern', 'hitfq']

def show_analisis_tab(draws):
    st.header("🔍 Analisis Nombor 4D")

    input_number = st.text_input("Masukkan Nombor 4D:", value="1234", max_chars=4, key="anlz_input")
    if len(input_number) != 4 or not input_number.isdigit():
        st.warning("⚠️ Sila masukkan nombor 4 digit yang sah.")
        return

    recent_n = st.slider("Jumlah draw terkini untuk analisis:", 10, len(draws), min(60, len(draws)), 5, key="anlz_recent")
    recent_draws = draws[-recent_n:]
    digits = list(input_number)

    # Paparan posisi
    st.markdown("**📌 Posisi Digit:**")
    cols = st.columns(4)
    for i, d in enumerate(digits):
        cols[i].markdown(f"**P{i+1}:** `{d}`")

    # Statistik
    st.markdown("---")
    st.subheader(f"📊 Statistik Digit (Last {recent_n} Draw)")
    last_hits = _get_last_hit(recent_draws)
    freqs = _get_frequency(recent_draws)

    stats, digit_score = [], 0
    for i, d in enumerate(digits):
        freq = freqs[i].get(d, 0)
        last_hit = last_hits.get(d, "N/A")
        status = "🔥 Hot" if freq >= (recent_n * 0.2) else "🧊 Cool"
        score = freq * 1.5 + (recent_n - last_hit) * 0.5 if isinstance(last_hit, int) else 0
        digit_score += score
        stats.append({
            "Posisi": f"P{i+1}", "Digit": d,
            "Kekerapan": freq, "Last Hit": last_hit, "Status": status, "Skor": round(score, 1)
        })
    st.dataframe(pd.DataFrame(stats), use_container_width=True)

    # Pattern Detection
    st.markdown("**🧠 Pola Dikesan:**")
    if digits[0] == digits[1] or digits[2] == digits[3]:
        st.info("💡 Terdapat pola kembar dalam nombor.")
    if digits == sorted(digits):
        st.info("📈 Pola menaik dikesan.")
    if digits == sorted(digits, reverse=True):
        st.info("📉 Pola menurun dikesan.")

    # Sejarah padan
    st.markdown("**🔁 Padanan Sejarah:**")
    matches = []
    for draw in draws:
        target = draw["number"]
        match_count = sum(1 for a, b in zip(digits, target) if a == b)
        if match_count >= 3:
            matches.append("".join(target))
    if matches:
        st.success(f"🎯 Nombor serupa (≥3 digit sepadan) pernah keluar: {', '.join(matches[:5])}")
    else:
        st.info("❌ Tiada padanan kuat ditemui dalam sejarah.")

    # Strategi padanan
    st.markdown("---")
    st.subheader("✅ Semakan Dalam Base Strategi")
    rows, matrix = [], []
    for strat in strategies:
        try:
            base = generate_base(recent_draws, method=strat, recent_n=recent_n)
            flags = ["✅" if digits[i] in base[i] else "❌" for i in range(4)]
            matrix.append([1 if x == "✅" else 0 for x in flags])
            rows.append({
                "Strategi": strat, "P1": flags[0], "P2": flags[1],
                "P3": flags[2], "P4": flags[3], "✅ Total": flags.count("✅")
            })
        except Exception:
            continue

    if not rows:
        st.warning("❗ Tiada strategi dapat dianalisis.")
        return

    df = pd.DataFrame(rows).sort_values("✅ Total", ascending=False)
    best = df.iloc[0]
    strategy_score = best["✅ Total"] * 2

    # Highlight posisi lemah
    weak_pos = [f"P{i+1}" for i, val in enumerate(df.iloc[0][["P1", "P2", "P3", "P4"]]) if val == "❌"]
    if weak_pos:
        st.warning(f"📉 Posisi lemah: {', '.join(weak_pos)}")

    st.success(f"🎯 Strategi terbaik: `{best['Strategi']}` dengan `{best['✅ Total']}/4` padanan digit.")
    st.markdown(f"### ⭐ Skor Strategi: `{strategy_score}/8`")
    st.dataframe(df, use_container_width=True)

    # Heatmap
    st.markdown("**🧊 Heatmap Strategi vs Posisi**")
    heat_df = pd.DataFrame(matrix, columns=["P1", "P2", "P3", "P4"], index=[r["Strategi"] for r in rows])
    fig, ax = plt.subplots()
    sns.heatmap(heat_df, cmap="YlGnBu", annot=True, cbar=False, ax=ax)
    st.pyplot(fig)

    # Total Score
    total_score = min(int(digit_score + strategy_score), 100)
    rating = "🟢 Bagus" if total_score >= 70 else "🟡 Sederhana" if total_score >= 40 else "🔴 Lemah"
    st.markdown("---")
    st.markdown(f"## 🧮 Skor Keseluruhan: `{total_score}/100` - {rating}")

    # Syor
    if total_score >= 70:
        st.success(f"✅ **Syor**: Nombor `{input_number}` disyorkan untuk dimainkan.")
    elif total_score >= 40:
        st.warning(f"⚠️ **Pertimbangan**: `{input_number}` boleh dicuba, tapi risiko sederhana.")
    else:
        st.error(f"❌ **Amaran**: `{input_number}` tidak sesuai dimainkan buat masa ini.")

    # Cadangan Nombor
    st.markdown("---")
    st.subheader("🤖 Cadangan Nombor Alternatif")

    hot_digits = list({d for pos in freqs for d, _ in pos.most_common(2)})
    suggestions = set()

    for i in range(4):
        for hot in hot_digits:
            if hot != digits[i]:
                new_num = digits.copy()
                new_num[i] = hot
                suggestions.add("".join(new_num))
            if len(suggestions) >= 6:
                break

    suggestions = sorted(suggestions)[:6]
    if suggestions:
        st.markdown("Cadangan berdasarkan pertukaran digit hot:")
        st.write(", ".join(f"`{s}`" for s in suggestions))
    else:
        st.info("❌ Tiada cadangan sesuai dijana.")

# Functions
def _get_last_hit(draws):
    last_seen = {}
    for i, draw in enumerate(draws[::-1]):
        for d in draw["number"]:
            if d not in last_seen:
                last_seen[d] = i + 1
    return last_seen

def _get_frequency(draws):
    pos_freq = [Counter() for _ in range(4)]
    for draw in draws:
        number = draw["number"]
        for i in range(4):
            pos_freq[i][number[i]] += 1
    return pos_freq