import streamlit as st
import itertools
import random
from collections import Counter

from utils import load_draws, load_base_from_file

def generate_predictions_from_base(base, max_preds=10):
    combos = [''.join(p) for p in itertools.product(*base)]
    return combos[:max_preds]

def generate_ai_predictions(draws_path="data/draws.txt", top_n=5):
    draws = load_draws(draws_path)
    
    # Kumpul semua digit dari setiap draw
    all_digits = []
    for draw in draws:
        num = draw.get("number", "")
        all_digits.extend(list(num))
    
    # Ambil 6 digit paling kerap
    freq = Counter(all_digits)
    hot_digits = [d for d, _ in freq.most_common(6)]

    preds = set()
    while len(preds) < top_n:
        preds.add("".join(random.sample(hot_digits, 4)))
    
    return sorted(preds)

def show_prediction_tab():
    st.subheader("🔮 Ramalan 4D Hari Ini")

    base = load_base_from_file()
    if not base:
        st.warning("❗ Base belum dijana. Sila update draw terlebih dahulu.")
        return

    st.markdown("### 📌 Ramalan Berdasarkan Base")
    base_preds = generate_predictions_from_base(base, max_preds=10)
    st.code('\n'.join(base_preds), language='text')

    st.markdown("### 🤖 Ramalan AI (Hot Digits)")
    ai_preds = generate_ai_predictions(top_n=5)
    st.code('\n'.join(ai_preds), language='text')