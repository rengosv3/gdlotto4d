# prediction.py

import itertools
import random
from collections import Counter

from utils import load_draws

def generate_predictions_from_base(base, max_preds=10):
    """
    Dari `base` (list of 4 lists), hasilkan kombinasi 4D dalam format string.
    Pulangkan maksimum `max_preds` nombor teratas (urut ikut cartesian).
    """
    # Semua kombinasi cartesian
    combos = [''.join(p) for p in itertools.product(*base)]
    return combos[:max_preds]

def generate_ai_predictions(draws_path="data/draws.txt", top_n=5):
    """
    Hasilkan `top_n` ramalan AI berdasarkan digit paling kerap muncul.
    """
    # Load history draws
    draws = load_draws(draws_path)
    # Kumpul semua digit daripada setiap nombor
    all_digits = [
        d
        for draw in draws
        for num in draw["numbers"]
        for d in num
    ]
    # Kira kekerapan
    freq = Counter(all_digits)
    # Ambil 6 digit paling kerap (hot digits)
    hot_digits = [d for d, _ in freq.most_common(6)]
    # Buat kombinasi rawak tanpa ulang
    preds = set()
    while len(preds) < top_n:
        preds.add("".join(random.sample(hot_digits, 4)))
    # Pulangkan disusun untuk konsistensi
    return sorted(preds)