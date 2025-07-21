import streamlit as st
import os
import re
import requests
from datetime import datetime, timedelta

BASE_PATH = "data/base.txt"
BASE_LAST_PATH = "data/base_last.txt"
DRAWS_PATH = "data/draws.txt"

# ========== Fungsi Utiliti ==========
def load_draws(file_path):
    if not os.path.exists(file_path):
        return []
    with open(file_path, "r") as f:
        lines = f.read().splitlines()
        return [{'date': line.split()[0], 'number': line.split()[1]} for line in lines if line.strip()]

def score_digits(draws):
    digit_count = {}
    for draw in draws[-10:]:  # Hanya ambil 10 draw terkini
        for d in draw['number']:
            digit_count[int(d)] = digit_count.get(int(d), 0) + 1
    sorted_digits = sorted(digit_count.items(), key=lambda x: -x[1])
    base = [d for d, _ in sorted_digits][:5]
    return [base] * 4  # Pulangkan 4 baris sama (Pick 1-4)

def save_base_to_file(base_digits, path):
    with open(path, "w") as f:
        for pick in base_digits:
            f.write(" ".join(map(str, pick)) + "\n")

# ========== Scrape Prize ==========
def get_1st_prize(date_str):
    url = f"https://gdlotto.net/results/ajax/_result.aspx?past=1&d={date_str}"
    try:
        resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=5)
        if resp.status_code != 200:
            return None
        html = resp.text
        match = re.search(r'id="1stPz">(\d{4})<', html)
        return match.group(1) if match else None
    except:
        return None

def update_draws(file_path=DRAWS_PATH, max_days_back=30):
    draws = load_draws(file_path)
    if not draws:
        last_date = datetime.today() - timedelta(days=max_days_back)
    else:
        last_date = datetime.strptime(draws[-1]['date'], "%Y-%m-%d")

    today = datetime.today()
    current = last_date + timedelta(days=1)
    added = []

    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'a') as f:
        while current <= today:
            date_str = current.strftime("%Y-%m-%d")
            prize = get_1st_prize(date_str)
            if prize:
                f.write(f"{date_str} {prize}\n")
                added.append({'date': date_str, 'number': prize})
            current += timedelta(days=1)

    if added:
        draws = load_draws(file_path)
        latest_base = score_digits(draws)
        save_base_to_file(latest_base, BASE_PATH)
        save_base_to_file(latest_base, BASE_LAST_PATH)

    return f"✔ {len(added)} draw baru ditambah." if added else "✔ Tiada draw baru ditambah."

# ========== Paparan Streamlit ==========
def display_draw_update():
    st.subheader("📥 Update Draw Terkini")

    if st.button("🚀 Kemaskini Auto (30 Hari Kebelakang)"):
        status = update_draws()
        st.success(status)

    draws = load_draws(DRAWS_PATH)
    if draws:
        st.markdown("### 📅 Sejarah Draw Terkini (Last 10)")
        for d in draws[-10:][::-1]:
            st.markdown(f"- {d['date']} : `{d['number']}`")
