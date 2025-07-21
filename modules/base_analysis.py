import streamlit as st
import os
from datetime import datetime

BASE_PATH = "data/base.txt"

# ===================== Base Loader =====================
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

# ===================== Base Editor =====================
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

# ===================== Draw Loader =====================
def load_draws(file_path='data/draws.txt'):
    draws = []
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) == 2:
                    draws.append({'date': parts[0], 'number': parts[1]})
    return draws

# ===================== Insight Paparan =====================
def display_last_number_insight():
    draws = load_draws()
    base_picks = load_base_from_file()

    if not draws or not base_picks:
        st.warning("Tiada data cabutan atau base digit tersedia.")
        return

    last_draw = draws[-1]
    number = last_draw["number"]
    date = last_draw["date"]

    st.markdown("### 📌 Insight Nombor Terakhir")
    st.markdown(f"📅 Nombor terakhir naik: `{number}` pada `{date}`")

    base_text = display_base_as_text(base_picks)
    st.markdown("📋 Base Digunakan:\n```\n" + base_text + "```")

    for i, digit_char in enumerate(number):
        digit = int(digit_char)
        base = base_picks[i]
        ranking = sorted(base, reverse=True).index(digit)+1 if digit in base else "-"
        base_check = "✅" if digit in base else "❌"
        cross_check = "✅"  # Dummy logic, boleh ganti dengan check sebenar jika ada
        if base_check == "✅" and cross_check == "✅":
            emoji = "🔥 Sangat berpotensi"
        elif cross_check == "✅":
            emoji = "👍 Berpotensi"
        else:
            emoji = "❌ Kurang"
        st.markdown(f"Pick {i+1}: Digit `{digit}` - Ranking #{ranking}, Base: {base_check}, Cross: {cross_check} → {emoji}")

    st.markdown("💡 **AI Insight:**")