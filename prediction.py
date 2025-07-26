import random
from collections import Counter
from utils import load_draws

def generate_ai_predictions(draws_path="data/draws.txt", top_n=5):
    draws = load_draws(draws_path)
    # kumpul semua digit
    all_digits = [d for draw in draws for num in draw["numbers"] for d in num]
    freq = Counter(all_digits)
    # ambil 6 digit paling kerap
    hot_digits = [d for d, _ in freq.most_common(6)]
    preds = set()
    while len(preds) < top_n:
        preds.add("".join(random.sample(hot_digits, 4)))
    return sorted(preds)