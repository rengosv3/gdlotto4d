# backtest.py
import pandas as pd
from strategies import generate_base

def match_insight(fp: str, base: list[list[str]], reverse: bool = False) -> list[str]:
    """
    Bandingkan hasil draw `fp` (string 4-digit) dengan `base`.
    Jika reverse=True, baca dari P4→P1.
    Pulangkan list 4 elemen “✅”/“❌”.
    """
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
    """
    Jalankan backtest:
      - draws: list of {'date', 'number'} berurutan waktu
      - strategy: 'frequency','gap','hybrid','qaisara','smartpattern'
      - recent_n: untuk strategi yang guna recent_n
      - arah: 'left' (P1→P4) atau 'right' (P4→P1)
      - backtest_rounds: bilangan draw terakhir diuji

    Pulangkan (DataFrame, matched_count) di mana matched_count
    adalah jumlah draw dengan sekurang-kurangnya satu “✅”.
    """
    total = len(draws)
    # keperluan minimum per strategi
    min_req = {'frequency':50, 'gap':120, 'hybrid':50, 'qaisara':60, 'smartpattern':60}
    req = min_req.get(strategy, 50)
    if total < backtest_rounds + req:
        raise ValueError(f"Not enough draws for backtest '{strategy}': "
                         f"need {backtest_rounds+req}, have {total}")

    reverse = True if arah == 'right' else False
    records = []

    # uji setiap draw terakhir
    for i in range(backtest_rounds):
        test_draw = draws[-(i+1)]
        past_draws = draws[:-(i+1)]

        # jana base
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

    # DataFrame terbalik (lama→baru)
    df = pd.DataFrame(records[::-1])
    # kira berapa draw ada sekurang-kurangnya satu ✅
    matched = sum('✅' in r['Insight'] for r in records)
    return df, matched