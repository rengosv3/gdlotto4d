import random
from .base_analysis import score_digits

def generate_predictions(base_digits, n=10):
    all_combinations = set()
    while len(all_combinations) < n:
        combo = ''.join(random.choice(base_digits[i]) for i in range(4))
        all_combinations.add(combo)
    return sorted(list(all_combinations))

def ai_tuner(draws):
    base_score = score_digits(draws, recent_n=30)
    filtered = [[d for d in pick if int(d) % 2 == 0 or d in '579'] for pick in base_score]
    return filtered