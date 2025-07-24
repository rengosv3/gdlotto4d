# app.py

import streamlit as st
import pandas as pd
import itertools
from datetime import datetime

# Import strategi ramalan
from strategies import generate_base

# Tab helper — pastikan modul ini wujud
from hit_frequency import show_hit_frequency_tab
from last_hit import show_last_hit_tab
from backtest import run_backtest
from wheelpick import show_wheelpick_tab

@st.cache_data
def load_draws(csv_path: str):
    df = pd.read_csv(csv_path, parse_dates=['date'])
    df['number'] = df['number'].astype(str).str.zfill(4)
    records = df[['date', 'number']].to_dict('records')
    return records, df

def main():
    st.set_page_config(page_title="4D Predictor", layout="wide")
    st.title("🎲 4D Predictor App")

    draw_list, df_draws = load_draws("data/draws.csv")

    st.sidebar.header("📊 Statistik Data")
    st.sidebar.write(f"Jumlah draw: {len(df_draws)}")
    st.sidebar.write(f"Tarikh terkini: {df_draws['date'].max().date()}")

    tabs = st.tabs([
        "Insight", "Ramalan", "Backtest",
        "Draw List", "Wheelpick",
        "Hit Frequency", "Last Hit"
    ])

    # --- Tab 1: Insight ---
    with tabs[0]:
        st.header("📈 Insight")
        df_plot = df_draws.copy()
        df_plot['num_int'] = df_plot['number'].astype(int)
        st.line_chart(df_plot.set_index('date')['num_int'])
        st.write("Trend nombor sebagai integer")

    # --- Tab 2: Ramalan ---
    with tabs[1]:
        st.header("🔮 Ramalan 4D")
        strategy = st.selectbox("Pilih strategi:", [
            'frequency', 'gap', 'hybrid',
            'coreboost', 'coreplus',
            'smartpattern', 'hitfq'
        ])
        recent_n = st.slider(
            "Bilangan draw terkini:", 30, 120, 60, step=5
        )

        try:
            base_digits = generate_base(
                draws=draw_list,
                method=strategy,
                recent_n=recent_n
            )
            st.write("Digit setiap posisi:", base_digits)

            combos = itertools.product(*base_digits)
            predictions = [''.join(d) for d in combos]
            st.write(f"Jumlah kombinasi: {len(predictions)}")
            st.text_area(
                "Senarai kombinasi:",
                '\n'.join(predictions),
                height=300
            )
        except Exception as e:
            st.error(f"⚠️ Ralat: {e}")

    # --- Tab 3: Backtest ---
    with tabs[2]:
        st.header("📊 Backtest")
        st.write("Uji prestasi strategi atas draw terakhir")
        backtest_n = st.slider(
            "Bilangan draw untuk backtest:", 30, 200, 60, step=10
        )
        if st.button("Run Backtest"):
            res = run_backtest(draw_list, backtest_n)
            st.dataframe(res)

    # --- Tab 4: Draw List ---
    with tabs[3]:
        st.header("📃 Senarai Draw")
        st.dataframe(df_draws)

    # --- Tab 5: Wheelpick ---
    with tabs[4]:
        st.header("🎡 Wheelpick")
        show_wheelpick_tab(draw_list)

    # --- Tab 6: Hit Frequency ---
    with tabs[5]:
        show_hit_frequency_tab(draw_list)

    # --- Tab 7: Last Hit ---
    with tabs[6]:
        show_last_hit_tab(df_draws)

if __name__ == "__main__":
    main()