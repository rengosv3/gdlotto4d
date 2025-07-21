import streamlit as st
import os
import random

BASE_PATH = "data/base.txt"
BASE_LAST_PATH = "data/base_last.txt"
SUPER_BASE_PATH = "data/base_super.txt"

def load_base_file(path):
    if os.path.exists(path):
        with open(path, "r") as f:
            lines = f.read().splitlines()
            return [list(map(int, line.strip().split())) for line in lines if line.strip()]
    else:
        return []

def load_last_number():
    if os.path.exists(BASE_LAST_PATH):
        with open(BASE_LAST_PATH, "r") as f:
            line = f.read().strip()
            if "-" in line:
                number, date = line.split("-")
                return number.strip(), date.strip()
    return None, None

def load_superbase_ranking():
    if os.path.exists(SUPER_BASE_PATH):
        with open(SUPER_BASE_PATH, "r") as f:
            return [line.strip() for line in f if line.strip()]
    return []

def get_digit_ranking(digit, ranking_list):
    for idx, entry in enumerate(ranking_list, start=1):
        if f"Digit {digit}" in entry:
            return idx
    return None

def cross_pick_analysis(pick_digit, base_digits):
    return any(pick_digit in pick for pick in base_digits)

def generate_ai_predictions(base_digits):
    predictions = set()
    while len(predictions) < 10:
        pick = [random.choice(random.choice(base_digits)) for _ in range(4)]
        predictions.add("".join(map(str, pick)))
    return sorted(predictions)

def display_ai_prediction():
    st.subheader("🤖 Ramalan AI (Top 10)")
    base_digits = load_base_file(BASE_PATH)
    if not base_digits:
        st.warning("Base digit belum dimasukkan.")
        return

    predictions = generate_ai_predictions(base_digits)
    st.markdown("#### 🎯 10 Nombor Ramalan:")
    st.markdown(" | ".join(predictions))

def display_last_number_insight():
    st.subheader("📌 Insight Nombor Terakhir")

    last_number, draw_date = load_last_number()
    base_digits = load_base_file(BASE_PATH)
    superbase_ranking = load_superbase_ranking()

    if not last_number or not base_digits:
        st.warning("Nombor terakhir atau base digit tidak lengkap.")
        return

    st.markdown(f"📅 Nombor terakhir naik: `{last_number}` pada `{draw_date}`")

    st.markdown("📋 Base Digunakan:")
    for i, pick in enumerate(base_digits, start=1):
        st.markdown(f"• Pick {i}: " + " ".join(map(str, pick)))

    result_lines = []
    for i, digit in enumerate(last_number):
        rank = get_digit_ranking(digit, superbase_ranking)
        base_hit = any(int(digit) in pick for pick in base_digits)
        cross_hit = cross_pick_analysis(int(digit), base_digits)

        remark = ""
        if base_hit and cross_hit:
            remark = "→ 🔥 Sangat berpotensi"
        elif not base_hit and cross_hit:
            remark = "→ 👍 Berpotensi"
        else:
            remark = "→ ❌ Lemah"

        result_lines.append(
            f"Pick {i+1}: Digit '{digit}' - Ranking #{rank if rank else '-'}, Base: {'✅' if base_hit else '❌'}, Cross: {'✅' if cross_hit else '❌'} {remark}"
        )

    st.markdown("<br>".join(result_lines), unsafe_allow_html=True)

    st.markdown("💡 **AI Insight:**")
