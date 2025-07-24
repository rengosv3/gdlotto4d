import streamlit as st
import pandas as pd
from collections import defaultdict
import os

def show_last_hit_tab(draws):
    st.header("📅 Last Hit Digit")

    # Slider untuk jumlah draw
    max_draws = max(10, min(120, len(draws)))
    n_draws = st.slider("Jumlah draw terkini:", 10, max_draws, 60, step=5, key="lh_draws")

    # Pilihan posisi
    position_checks = [
        ("P1", st.checkbox("P1", value=True, key="lh_p1")),
        ("P2", st.checkbox("P2", value=True, key="lh_p2")),
        ("P3", st.checkbox("P3", value=True, key="lh_p3")),
        ("P4", st.checkbox("P4", value=True, key="lh_p4")),
    ]
    selected_positions = [i for i, (_, checked) in enumerate(position_checks) if checked]

    if not selected_positions:
        st.warning("⚠️ Sila pilih sekurang-kurangnya satu posisi.")
        return

    # Ambil draw terkini
    recent_draws = draws[-n_draws:]
    last_hit_map = defaultdict(lambda: {"date": None, "index": None})

    # Cari tarikh terakhir digit muncul
    for idx in reversed(range(len(recent_draws))):
        draw = recent_draws[idx]
        num_str = str(draw["number"]).zfill(4)  # Pastikan 4 digit

        for i in selected_positions:
            if i < len(num_str):
                digit = num_str[i]
                if last_hit_map[digit]["date"] is None:
                    last_hit_map[digit]["date"] = draw["date"]
                    last_hit_map[digit]["index"] = idx

    # Sediakan dataframe
    all_digits = [f"{i}" for i in range(10)]
    rows = []
    for digit in all_digits:
        info = last_hit_map.get(digit, {"date": None, "index": None})
        date_hit = info["date"]
        skipped = len(recent_draws) - 1 - info["index"] if info["index"] is not None else n_draws
        rows.append({
            "Number": digit,
            "Last Date Hit": date_hit if date_hit else "—",
            "Games Skipped": skipped
        })

    df = pd.DataFrame(rows)
    df.sort_values(["Games Skipped", "Number"], ascending=[False, True], inplace=True)
    df.insert(0, "Rank", range(1, len(df) + 1))
    st.dataframe(df, use_container_width=True)

    # Simpan ke fail
    os.makedirs("data", exist_ok=True)
    df.to_csv("data/last_hit.txt", index=False, sep="\t")
    st.success("📁 Disimpan ke `data/last_hit.txt`")