import pandas as pd
from collections import Counter, defaultdict
from wheelpick import get_like_dislike_digits

def generate_base(draws, method='frequency', recent_n=50):
    total = len(draws)

    requirements = {
        'frequency': recent_n,
        'gap': recent_n,
        'hybrid': recent_n,
        'break': 60,
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

    # === BREAK ===
    def break_method(draws_slice, n):
        recent_draws = draws_slice[-n:]
        result = []

        for pos in range(4):
            counter = Counter()
            last_seen = {str(i): -1 for i in range(10)}
            total_slots = 0

            for idx, draw in enumerate(reversed(recent_draws)):
                digit = str(int(draw['number'][pos]))
                counter[digit] += 1
                total_slots += 1
                if last_seen[digit] == -1:
                    last_seen[digit] = idx

            rows = []
            for d in range(10):
                digit = str(d)
                freq = counter[digit] / total_slots * 100
                skipped = last_seen[digit] if last_seen[digit] != -1 else n
                rows.append({
                    "Digit": digit,
                    "Hit Frequency (%)": freq,
                    "Games Skipped": skipped
                })

            df = pd.DataFrame(rows)
            df.sort_values("Hit Frequency (%)", ascending=False, inplace=True)
            df.reset_index(drop=True, inplace=True)
            df["Rank"] = df.index + 1
            top_digits = df.iloc[5:10]["Digit"].tolist()
            result.append(top_digits)

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

    # === SMARTPATTERN ===
    def smartpattern_method(draws_slice):
        settings = [
            ('break', 60),
            ('hybrid', 45),
            ('frequency', 50),
            ('hybrid', 35),
        ]
        result = []
        for idx, (strat, n) in enumerate(settings):
            base = generate_base(draws_slice, strat, n)
            result.append(base[idx])
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

    # === MAIN STRATEGY SWITCH ===
    if method == 'frequency':
        return freq_method(draws, recent_n)
    elif method == 'gap':
        return gap_method(draws, recent_n)
    elif method == 'hybrid':
        return hybrid_method(draws, recent_n)
    elif method == 'break':
        return break_method(draws, 60)
    elif method == 'smartpattern':
        return smartpattern_method(draws)
    elif method == 'hitfq':
        return hitfq_method(draws, recent_n)
    else:
        raise ValueError(f"Unsupported method '{method}'")