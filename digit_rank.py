import streamlit as st
import pandas as pd
from collections import Counter, defaultdict
import os

def show_digit_rank_tab(draws):
    st.header("📊 Digit Rank")

    n_draws = st.slider("Jumlah draw terkini:", 10, min(120, len(draws)), 60, step=5, key="dr_draws")

    pos_check = {
        0: st.checkbox("P1", True, key="dr_p1"),
        1: st.checkbox("P2", True, key="dr_p2"),
        2: st.checkbox("P3", True, key="dr_p3"),
        3: st.checkbox("P4", True, key="dr_p4"),
    }
    selected_positions = [i for i, v in pos_check.items() if v]

    if not selected_positions:
        st.warning("⚠️ Sila pilih sekurang-kurangnya satu posisi.")
        return

    recent_draws = draws[-n_draws:]
    os.makedirs("data", exist_ok=True)

    for pos in selected_positions:
        # Kira Hit Frequency
        counter = Counter()
        total_slots = 0

        for draw in recent_draws:
            number = f"{int(draw['number']):04d}"
            digit = f"{int(number[pos]):02d}"
            counter[digit] += 1
            total_slots += 1

        freq_df = pd.DataFrame(counter.items(), columns=["Digit", "Times Hit"])
        freq_df["Hit Frequency"] = freq_df["Times Hit"] / total_slots * 100

        # Kira Last Hit
        last_hit = defaultdict(lambda: {"index": None})
        for idx in reversed(range(len(recent_draws))):
            number = f"{int(recent_draws[idx]['number']):04d}"
            digit = f"{int(number[pos]):02d}"
            if last_hit[digit]["index"] is None:
                last_hit[digit]["index"] = idx

        # Gabung DataFrame
        rows = []
        for d in range(10):
            digit = f"{d:02d}"
            freq_row = freq_df[freq_df["Digit"] == digit]
            freq = float(freq_row["Hit Frequency"]) if not freq_row.empty else 0.0
            skipped = len(recent_draws) - 1 - last_hit[digit]["index"] if last_hit[digit]["index"] is not None else n_draws

            if freq >= 12.0 and skipped <= 3:
                status = "🔥 Hot"
            elif freq <= 5.0 and skipped >= 20:
                status = "🧊 Cold"
            elif skipped >= 25:
                status = "🧓 Stale"
            elif skipped <= 2:
                status = "🌱 Fresh"
            else:
                status = "—"

            rows.append({
                "Digit": digit,
                "Hit Frequency (%)": round(freq, 1),
                "Games Skipped": skipped,
                "Status": status
            })

        df = pd.DataFrame(rows)
        df.sort_values(["Status", "Games Skipped"], ascending=[True, False], inplace=True)
        df.insert(0, "Rank", range(1, len(df) + 1))

        st.subheader(f"📌 Posisi P{pos + 1}")
        st.dataframe(df, use_container_width=True)

        path = f"data/digit_rank_p{pos+1}.txt"
        df.to_csv(path, index=False, sep="\t")
        st.success(f"📁 Disimpan ke `{path}`")