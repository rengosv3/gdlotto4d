import streamlit as st
import pandas as pd
from strategies import generate_base
from collections import Counter

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
    min_req = {'frequency':50, 'gap':120, 'hybrid':50, 'qaisara':60, 'smartpattern':60, 'break':50, 'hitfq':50}
    req = min_req.get(strategy, 50)
    if total < backtest_rounds + req:
        raise ValueError(f"Not enough draws for backtest '{strategy}': need {backtest_rounds+req}, have {total}")

    reverse = (arah == 'right')
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
    matched = sum(all(mark == "✅" for mark in row['Insight'].split()) for _, row in df.iterrows())
    return df, matched

strategies = ['frequency', 'polarity_shift', 'hybrid', 'break', 'smartpattern', 'hitfq']

def evaluate_strategies(draws: list[dict], test_n: int = 20) -> pd.DataFrame:
    results = []
    total_draws = len(draws)

    for method in strategies:
        correct_total = 0
        tested = 0
        min_req = {'frequency':50, 'gap':120, 'hybrid':50, 'qaisara':60, 'smartpattern':60, 'break':50, 'hitfq':50}
        req = min_req.get(method, 50)
        if total_draws < test_n + req:
            continue

        for i in range(test_n):
            idx = total_draws - (test_n - i)
            subset = draws[:idx]
            actual = draws[idx]['number']
            try:
                base = generate_base(subset, method=method, recent_n=50)
            except Exception:
                continue
            match_count = sum(actual[pos] in base[pos] for pos in range(4))
            correct_total += match_count
            tested += 1

        avg_hit = (correct_total / (tested * 4) * 100) if tested > 0 else 0
        results.append({
            'Strategy': method,
            'Avg Hit Rate': round(avg_hit, 2),
            'Tested Draws': tested,
            'Total Match': correct_total
        })

    return pd.DataFrame(results).sort_values(by='Avg Hit Rate', ascending=False).reset_index(drop=True)

def show_backtest_tab():
    st.header("🧪 Backtest Base")
    draws = st.session_state.get('draws') or []  # assume draws passed to session_state
    if not draws:
        st.warning("⚠️ Sila kemaskini draws dahulu.")
        return

    arah = st.radio("Arah:", ["Kiri→Kanan", "Kanan→Kiri"], key="bt_dir")
    strat = st.selectbox("Strategi:", strategies, key="bt_strat")
    recent_n = st.slider("Draw untuk base:", 5, len(draws), 30, 5, key="bt_n")
    rounds = st.slider("Bilangan backtest:", 5, 50, 10, key="bt_rounds")

    if st.button("🚀 Jalankan Backtest", key="bt_run"):
        try:
            df_bt, matched = run_backtest(
                draws,
                strategy=strat,
                recent_n=recent_n,
                arah='right' if arah == "Kanan→Kiri" else 'left',
                backtest_rounds=rounds
            )
            st.success(f"🎯 Matched full 4️⃣ ✅: {matched} daripada {rounds}")
            st.dataframe(df_bt, use_container_width=True)

            st.markdown("---")
            st.subheader("📊 Evaluasi Semua Strategi (Top Hit Rate)")
            df_eval = evaluate_strategies(draws, test_n=rounds)
            st.dataframe(df_eval, use_container_width=True)
            if not df_eval.empty:
                best = df_eval.iloc[0]
                st.success(f"🎯 Strategi terbaik: `{best['Strategy']}` dengan purata hit rate {best['Avg Hit Rate']}%")
        except Exception as e:
            st.error(str(e))