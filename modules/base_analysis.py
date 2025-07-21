import streamlit as st
import os

BASE_PATH = "data/base.txt"

def load_base_from_file():
    if os.path.exists(BASE_PATH):
        with open(BASE_PATH, "r") as f:
            lines = f.read().splitlines()
            return [list(map(int, line.strip().split())) for line in lines if line.strip()]
    else:
        return []

def save_base_to_file(picks):
    with open(BASE_PATH, "w") as f:
        for pick in picks:
            f.write(" ".join(map(str, pick)) + "\n")

def display_base_as_text(picks):
    text = ""
    for i, pick in enumerate(picks, start=1):
        text += f"• Pick {i}: " + " ".join(map(str, pick)) + "\n"
    return text

def display_base_interface():
    st.subheader("📊 Base Digit Digunakan")

    base_picks = load_base_from_file()

    if not base_picks:
        st.warning("Tiada base digit ditemui. Sila masukkan digit secara manual.")
        base_picks = [[0, 0, 0, 0, 0] for _ in range(4)]

    editable_base = []
    for i in range(4):
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            d1 = st.number_input(f"Pick {i+1} - D1", min_value=0, max_value=9, value=base_picks[i][0], key=f"{i}_0")
        with col2:
            d2 = st.number_input(f"Pick {i+1} - D2", min_value=0, max_value=9, value=base_picks[i][1], key=f"{i}_1")
        with col3:
            d3 = st.number_input(f"Pick {i+1} - D3", min_value=0, max_value=9, value=base_picks[i][2], key=f"{i}_2")
        with col4:
            d4 = st.number_input(f"Pick {i+1} - D4", min_value=0, max_value=9, value=base_picks[i][3], key=f"{i}_3")
        with col5:
            d5 = st.number_input(f"Pick {i+1} - D5", min_value=0, max_value=9, value=base_picks[i][4], key=f"{i}_4")
        editable_base.append([d1, d2, d3, d4, d5])

    if st.button("💾 Simpan Base"):
        save_base_to_file(editable_base)
        st.success("Base digit berjaya disimpan.")

    st.markdown("### 📋 Base Sekarang")
    st.text(display_base_as_text(editable_base))

def display_last_number_insight():
    st.subheader("📌 Insight Nombor Terakhir")

    last_number = None
    last_date = "Tidak diketahui"
    draws_path = "data/draws.txt"

    if os.path.exists(draws_path):
        with open(draws_path, "r") as f:
            lines = f.read().splitlines()
            if lines:
                last_line = lines[-1]
                parts = last_line.strip().split()
                if len(parts) == 2:
                    last_date = parts[0].strip()
                    last_number = parts[1].strip()

    if not last_number:
        st.warning("❗ Nombor terakhir tidak dapat dibaca dari draws.txt")
        return

    picks = load_base_from_file()

    insight_text = f"""
📅 Nombor terakhir naik: `{last_number}` pada `{last_date}`  
📋 Base Digunakan:
{display_base_as_text(picks)}
"""
    st.markdown(insight_text)