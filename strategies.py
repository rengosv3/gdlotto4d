# strategies.py

import pandas as pd
from collections import Counter, defaultdict
from wheelpick import get_like_dislike_digits

def generate_base(draws, method='frequency', recent_n=50):
    total = len(draws)

    requirements = {
        'frequency': recent_n,
        'gap': 120,
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
        for draw in draws_slice[-120:]:
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
        # Create digit_rank directly from draws (no digit_rank.txt needed)
        all_digits = [f"{i:02d}" for i in range(100)]
        recent_draws = draws[-60:]
        
        count = defaultdict(int)
        last_seen = {d: -1 for d in all_digits}

        for idx, draw in enumerate(reversed(recent_draws)):
            for d in draw['number']:
                count[d] += 1
                if last_seen[d] == -1:
                    last_seen[d] = idx

        digit_rank_df = pd.DataFrame(all_digits, columns=["Digit"])
        digit_rank_df["Hit Count"] = digit_rank_df["Digit"].map(count).fillna(0).astype(int)
        digit_rank_df["Hit Frequency (%)"] = digit_rank_df["Hit Count"] / 60 * 100
        digit_rank_df["Games Skipped"] = digit_rank_df["Digit"].map(lambda d: last_seen[d] if last_seen[d] != -1 else 60)

        digit_rank_df = digit_rank_df.sort_values(by="Hit Frequency (%)", ascending=False).reset_index(drop=True)
        digit_rank_df.index += 1
        digit_rank_df.insert(0, "Rank", digit_rank_df.index)

        # Ambil Rank 6–10 sahaja
        top_digits = digit_rank_df.iloc[5:10]["Digit"].tolist()

        # Guna sama untuk keempat-empat posisi
        return [top_digits.copy() for _ in range(4)]

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
            top = c.most_common()
            ranked = sorted(top, key=lambda x: (-x[1], int(x[0])))
            base.append([d for d, _ in ranked[:5]])
        return base