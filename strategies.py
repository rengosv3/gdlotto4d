# strategies.py

import itertools
from collections import Counter
import pandas as pd
from wheelpick import get_like_dislike_digits

def generate_base(draws, method='frequency', recent_n=50):
    total = len(draws)

    requirements = {
        'frequency': recent_n,
        'gap': 120,
        'hybrid': recent_n,
        'break': 60,           # ⬅️ ubah nama dari qaisara ke break
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
        return [[d for d,_ in c.most_common(5)] for c in counters]

    def gap_method(draws_slice):
        freq_120 = [Counter() for _ in range(4)]
        for draw in draws_slice[-120:]:
            for i, d in enumerate(draw['number']):
                freq_120[i][d] += 1
        top_digits = []
        for cnt in freq_120:
            mc = cnt.most_common(10)
            if len(mc) < 3:
                top_digits.append([d for d,_ in mc])
            else:
                filtered = [d for d,_ in mc if d not in (mc[0][0], mc[-1][0])]
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
            excluded = set([d for d,_ in recent_top[i].most_common(2)]) | recent_seen[i]
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
            combined.append([d for d,_ in cnt.most_common(5)])
        return combined

    if method == 'break':  # ⬅️ Nama baru strategi
        df = pd.read_csv("data/digit_rank.txt", sep="\t")
        df["Digit"] = df["Digit"].astype(str)
        df["Position"] = df.index % 4  # Anggap 4 posisi berulang

        base = []
        for pos in range(4):
            group = df[df["Position"] == pos]["Digit"].tolist()
            group_6_10 = group[5:10]  # Rank 6–10
            base.append(group_6_10)

        like, dislike = get_like_dislike_digits(draws, recent_n=60)

        for i in range(4):
            base[i] = [d for d in base[i] if d in like and d not in dislike]

            if not base[i]:
                fallback = df[df["Position"] == i]["Digit"].tolist()[5:15]
                base[i] = [d for d in fallback if d not in dislike][:5]

            if len(base[i]) < 5:
                extra = df[df["Position"] == i]["Digit"].tolist()[5:15]
                for d in extra:
                    if d not in base[i] and d not in dislike:
                        base[i].append(d)
                    if len(base[i]) == 5:
                        break

        return base

    if method == 'smartpattern':
        settings = [
            ('break', 60),        # ⬅️ guna 'break'
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
            top = c.most_common()
            ranked = sorted(top, key=lambda x: (-x[1], int(x[0])))
            base.append([d for d, _ in ranked[:5]])
        return base