import pandas as pd
from strategies import generate_base
def match_insight(fp: str, base: list[list[str]], reverse: bool = False) -> list[str]:
    digits = list(fp)
    if reverse:
        digits = digits[::-1]
    return ["✅" if digits[i] in base[i] else "❌" for i in range(4)]

def run_backtest(
    draws: list[dict],
    strategy: str = 'hybrid',
    recent_n: int = 50,
    arah: str = 'left',
    backtest_rounds: int = 10
) -> tuple[pd.DataFrame, int]:
    total = len(draws)
    min_req = {'frequency':50, 'gap':120, 'hybrid':50, 'qaisara':60, 'smartpattern':60}
    req = min_req.get(strategy, 50)
    if total < backtest_rounds + req:
        raise ValueError(f"Not enough draws for backtest '{strategy}': "
                         f"need {backtest_rounds+req}, have {total}")

    reverse = True if arah == 'right' else False
    records = []

    for i in range(backtest_rounds):
        test_draw = draws[-(i+1)]
        past_draws = draws[:-(i+1)]

        if strategy == 'smartpattern':
            base = generate_base(past_draws, method=strategy)
        else:
            base = generate_base(past_draws, method=strategy, recent_n=recent_n)

        insight = match_insight(test_draw['number'], base, reverse)
        records.append({
            'Tarikh': test_draw['date'],
            'Result 1st': test_draw['number'],
            'Insight': ' '.join(f"P{j+1}:{s}" for j, s in enumerate(insight))
        })

    df = pd.DataFrame(records[::-1])

    # ✅ Betulkan: Kira draw yang full 4 ✅ sahaja
    matched = sum(all(s.endswith("✅") for s in r['Insight'].split()) for r in records)
    return df, matched

# ========================================================
# FUNGSI TAMBAHAN: EVALUATE SEMUA STRATEGI
# ========================================================

strategies = ['frequency', 'polarity_shift', 'hybrid', 'break', 'smartpattern', 'hitfq']

def evaluate_strategies(draws, test_n=20):
    results = []

    for method in strategies:
        try:
            correct_total = 0
            tested = 0

            for i in range(test_n):
                subset = draws[:-(test_n - i)]
                actual = draws[-(test_n - i)]['number']

                try:
                    base = generate_base(subset, method)
                except Exception:
                    continue

                match = sum([actual[pos] in base[pos] for pos in range(4)])
                correct_total += match
                tested += 1

            avg_hit = correct_total / (tested * 4) if tested > 0 else 0
            results.append({
                'Strategy': method,
                'Avg Hit Rate': round(avg_hit * 100, 2),
                'Tested Draws': tested,
                'Total Match': correct_total
            })

        except Exception as e:
            results.append({
                'Strategy': method,
                'Avg Hit Rate': 0,
                'Tested Draws': 0,
                'Total Match': 0,
                'Error': str(e)
            })

    return pd.DataFrame(results).sort_values(by='Avg Hit Rate', ascending=False).reset_index(drop=True)