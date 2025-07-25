import streamlit as st
import pandas as pd
from collections import defaultdict
import os

def show_last_hit_tab(draws):
    st.header("📅 Last Hit Digit")

    # Slider draw
    n_draws = st.slider("Jumlah draw terkini:", 10, min(120, len(draws)), 60, step=5, key="lh_draws")

    # Pilihan posisi
    pos_check = {
        0: st.checkbox("P1", True, key="lh_p1"),
        1: st.checkbox("P2", True, key="lh_p2"),
        2: st.checkbox("P3", True, key="lh_p3"),
        3: st.checkbox("P4", True, key="lh_p4"),
    }
    selected_positions = [i for i, v in pos_check.items() if v]

    if not selected_positions:
        st.warning("⚠️ Sila pilih sekurang-kurangnya satu posisi.")
        return

    # Ambil draw terkini
    recent_draws = draws[-n_draws:]

    # Simpan tarikh terakhir setiap digit muncul
    last_hit = defaultdict(lambda: {"date": None, "index": None})

    for idx in reversed(range(len(recent_draws))):
        draw = recent_draws[idx]
        number = str(draw["number"])  # pastikan string
        for i in selected_positions:
            digit = number[i]
            if last_hit[digit]["date"] is None:
                last_hit[digit]["date"] = draw["date"]
                last_hit[digit]["index"] = idx

    # Susun data
    rows = []
    for d in range(10):
        digit = str(d)
        info = last_hit.get(digit, {"date": None, "index": None})
        skipped = len(recent_draws) - 1 - info["index"] if info["index"] is not None else n_draws
        rows.append({
            "Number": f"{d:02d}",
            "Last Date Hit": info["date"] if info["date"] else "—",
            "Games Skipped": skipped
        })

    df = pd.DataFrame(rows)
    df.sort_values(["Games Skipped", "Number"], ascending=[False, True], inplace=True)
    df.insert(0, "Rank", range(1, len(df) + 1))

    # Papar dan simpan
    st.dataframe(df, use_container_width=True)
    os.makedirs("data", exist_ok=True)
    df.to_csv("data/last_hit.txt", index=False, sep="\t")
    st.success("📁 Disimpan ke `data/last_hit.txt`")