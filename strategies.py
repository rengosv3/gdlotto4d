# strategies.py
import itertools
from collections import Counter

def generate_base(draws, method='frequency', recent_n=50):
    """
    Returns a list of 4 lists (one per digit position), each containing top-5 candidate digits.
    methods: 'frequency','gap','hybrid','qaisara','smartpattern','hitfq'
    recent_n: number of latest draws to consider (where applicable)
    Raises ValueError on insufficient data or unknown method.
    """
    total = len(draws)
    # Minimum requirements
    requirements = {
        'frequency': recent_n,
        'gap': 120,
        'hybrid': recent_n,
        'qaisara': 60,
        'smartpattern': 60,
        'hitfq': recent_n
    }
    if method not in requirements:
        raise ValueError(f"Unknown strategy '{method}'")
    if total < requirements[method]:
        raise ValueError(f"Not enough draws for '{method}' (need {requirements[method]}, have {total})")

    # ---------- Helper methods ----------
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

    # ---------- Strategies ----------
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

    if method == 'qaisara':
        f = freq_method(draws, recent_n)
        g = gap_method(draws)
        h = generate_base(draws, 'hybrid', recent_n)
        final = []
        for pos in range(4):
            score = Counter()
            score.update(f[pos])
            score.update(g[pos])
            score.update(h[pos])
            ranked = score.most_common()
            if len(ranked) > 2:
                ranked = ranked[1:-1]  # drop top & bottom
            final.append([d for d,_ in ranked[:5]])
        return final

    if method == 'smartpattern':
        settings = [
            ('qaisara', 60),   # for P1
            ('hybrid', 45),    # for P2
            ('frequency', 50), # for P3
            ('hybrid', 35),    # for P4
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