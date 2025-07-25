import pandas as pd
from collections import Counter, defaultdict
from wheelpick import get_like_dislike_digits

def generate_base(draws, method='frequency', recent_n=50):
    total = len(draws)

    requirements = {
        'frequency': recent_n,
        'gap': 30,
        'hybrid': recent_n,
        'break': 60,
        'smartpattern': 60,
        'hitfq': recent_n
    }

    if method not in requirements:
        raise ValueError(f"Unknown strategy '{method}'")
    if total < requirements[method]:
        raise ValueError(f"Not enough draws for '{method}' (need {requirements[method]}, have {total})")

    def freq_method(draws_slice, n):
        counters = [Counter() for _ in range(4)]
        for d in draws_slice[-n:]:
            for i, digit in enumerate(d['number']):
                counters[i][digit] += 1
        return [[d for d, _ in c.most_common(5)] for c in counters]

    def gap_method(draws_slice):
        freq_120 = [Counter() for _ in range(4)]
        for draw in draws_slice[-30:]:
            for i, d in enumerate(draw['number']):
                freq_120[i][d] += 1
        top_digits = []
        for cnt in freq_120:
            mc = cnt.most_common(10)
            if len(mc) < 3:
                top_digits.append([d for d, _ in mc])
            else:
                filtered = [d for d, _ in mc if d not in (mc[0][0], mc[-1][0])]
                top_digits.append(filtered[:8])
        recent10 = draws_slice[-10:]
        recent_top = [Counter() for _ in range(4)]
        recent_seen = [set() for _ in range(4)]
        for draw in recent10:
            for i, d in enumerate(draw['number']):
                recent_top[i][d] += 1
                recent_seen[i].add(d)
        gap_res = []
        for i in range(4):
            excluded = set([d for d, _ in recent_top[i].most_common(2)]) | recent_seen[i]
            final = [d for d in top_digits[i] if d not in excluded]
            gap_res.append(final[:5])
        return gap_res

    if method == 'frequency':
        return freq_method(draws, recent_n)

    if method == 'gap':
        return gap_method(draws)

    if method == 'hybrid':
        f = freq_method(draws, recent_n)
        g = gap_method(draws)
        combined = []
        for f_list, g_list in zip(f, g):
            cnt = Counter(f_list + g_list)
            combined.append([d for d, _ in cnt.most_common(5)])
        return combined

    if method == 'break':
        recent_draws = draws[-recent_n:]
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
                skipped = last_seen[digit] if last_seen[digit] != -1 else 60
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

    if method == 'smartpattern':
        settings = [
            ('break', 60),
            ('hybrid', 45),
            ('frequency', 50),
            ('hybrid', 35),
        ]
        result = []
        for idx, (strat, n) in enumerate(settings):
            base = generate_base(draws, strat, n)
            result.append(base[idx])
        return result

    if method == 'hitfq':
        recent_draws = draws[-recent_n:]
        counters = [Counter() for _ in range(4)]
        for draw in recent_draws:
            for i, digit in enumerate(draw['number']):
                counters[i][digit] += 1
        base = []
        for c in counters:
            ranked = sorted(c.items(), key=lambda x: (-x[1], int(x[0])))
            base.append([d for d, _ in ranked[:5]])
        return base