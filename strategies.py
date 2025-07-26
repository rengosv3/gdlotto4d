import os
import pandas as pd
from collections import Counter, defaultdict
from itertools import product
from wheelpick import get_like_dislike_digits

def generate_base(draws, method='frequency', recent_n=50):
    total = len(draws)

    requirements = {
        'frequency': recent_n,
        'gap': recent_n,
        'hybrid': recent_n,
        'break': 0,  # sebab baca dari fail digit_rank_p*.txt
        'smartpattern': 60,
        'hitfq': recent_n
    }

    if method not in requirements:
        raise ValueError(f"Unknown strategy '{method}'")
    if total < requirements[method]:
        raise ValueError(f"Not enough draws for '{method}' (need {requirements[method]}, have {total})")

    # === FREQUENCY ===
    def freq_method(draws_slice, n):
        counters = [Counter() for _ in range(4)]
        for d in draws_slice[-n:]:
            for i, digit in enumerate(d['number']):
                counters[i][digit] += 1
        return [[d for d, _ in c.most_common(5)] for c in counters]

    # === GAP ===
    def gap_method(draws_slice, n):
        draws_used = draws_slice[-n:]
        last_seen = [defaultdict(lambda: -1) for _ in range(4)]

        for idx, draw in enumerate(reversed(draws_used)):
            for pos, digit in enumerate(draw['number']):
                if last_seen[pos][digit] == -1:
                    last_seen[pos][digit] = idx

        result = []
        for pos in range(4):
            gap_list = [(str(d), last_seen[pos][str(d)]) for d in range(10)]
            gap_sorted = sorted(gap_list, key=lambda x: -x[1])
            top5 = [d for d, _ in gap_sorted[:5]]
            result.append(top5)

        return result

    # === HYBRID ===
    def hybrid_method(draws_slice, n):
        f = freq_method(draws_slice, n)
        g = gap_method(draws_slice, n)
        combined = []
        for f_list, g_list in zip(f, g):
            cnt = Counter(f_list + g_list)
            combined.append([d for d, _ in cnt.most_common(5)])
        return combined

    # === BREAK ===
    def break_method_from_digit_rank():
        result = []

        for i in range(1, 5):
            filepath = f"data/digit_rank_p{i}.txt"
            if not os.path.exists(filepath):
                raise FileNotFoundError(f"{filepath} tidak wujud")

            df = pd.read_csv(filepath, sep="\t")
            subset = df[(df['Rank'] >= 6) & (df['Rank'] <= 10)]
            digits = subset["Digit"].astype(str).tolist()
            result.append(digits)  # ⬅️ Simpan 5 digit ikut posisi

        return result  # ⬅️ Bukan kombinasi 4D, tapi 5 digit setiap posisi

    # === SMARTPATTERN ===
    def smartpattern_method(draws_slice):
        strategies = [
            generate_base(draws_slice, 'frequency', 50),
            generate_base(draws_slice, 'gap', 50),
            generate_base(draws_slice, 'hybrid', 40),
            generate_base(draws_slice, 'hitfq', 30),
        ]

        result = []
        for pos in range(4):
            votes = Counter()
            for strat in strategies:
                for digit in strat[pos]:
                    votes[digit] += 1
            top5 = [d for d, _ in votes.most_common(5)]
            result.append(top5)

        return result

    # === HIT FREQUENCY ===
    def hitfq_method(draws_slice, n):
        recent_draws = draws_slice[-n:]
        counters = [Counter() for _ in range(4)]
        for draw in recent_draws:
            for i, digit in enumerate(draw['number']):
                counters[i][digit] += 1
        base = []
        for c in counters:
            ranked = sorted(c.items(), key=lambda x: (-x[1], int(x[0])))
            base.append([d for d, _ in ranked[:5]])
        return base

    # === STRATEGY DISPATCH ===
    if method == 'frequency':
        return freq_method(draws, recent_n)
    elif method == 'gap':
        return gap_method(draws, recent_n)
    elif method == 'hybrid':
        return hybrid_method(draws, recent_n)
    elif method == 'break':
        return break_method_from_digit_rank()
    elif method == 'smartpattern':
        return smartpattern_method(draws)
    elif method == 'hitfq':
        return hitfq_method(draws, recent_n)
    else:
        raise ValueError(f"Unsupported method '{method}'")