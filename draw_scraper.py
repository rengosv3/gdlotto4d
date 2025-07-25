# draw_scraper.py
import os
import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

from utils import load_draws, save_base_to_file
from strategies import generate_base  # pastikan nanti anda ada strategies.py

def get_1st_prize(date_str: str) -> str | None:
    """
    Scrape 1st prize 4D untuk tarikh YYYY-MM-DD.
    Pulangkan string 4-digit jika jumpa, else None.
    """
    url = f"https://gdlotto.net/results/ajax/_result.aspx?past=1&d={date_str}"
    try:
        resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        if resp.status_code != 200:
            print(f"❌ Status bukan 200 untuk {date_str}: {resp.status_code}")
            return None
        soup = BeautifulSoup(resp.text, "html.parser")
        prize_tag = soup.find("span", id="1stPz")
        txt = prize_tag.text.strip() if prize_tag else ""
        if txt.isdigit() and len(txt) == 4:
            return txt
        print(f"❌ Tidak jumpa 1st Prize untuk {date_str}")
    except Exception as e:
        print(f"❌ Ralat semasa request untuk {date_str}: {e}")
    return None

def update_draws(file_path: str = 'data/draws.txt', max_days_back: int = 61) -> str:
    """
    Update 'data/draws.txt' dengan draw baru sehingga semalam.
    Juga generate base_last.txt & base.txt menggunakan strategies.generate_base.
    """
    draws = load_draws(file_path)
    existing = {d['date'] for d in draws}

    # Tentukan tarikh mula scrape
    if draws:
        last_date = datetime.strptime(draws[-1]['date'], "%Y-%m-%d")
    else:
        last_date = datetime.today() - timedelta(days=max_days_back)
    yesterday = datetime.today() - timedelta(days=1)
    current = last_date + timedelta(days=1)

    added = []
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    # Langkah 1: base_last dari semua draws kecuali terakhir
    if len(draws) >= 51:
        base_before = generate_base(draws[:-1], method='frequency', recent_n=50)
        save_base_to_file(base_before, 'data/base_last.txt')
    else:
        # delete kalau wujud
        last_fp = 'data/base_last.txt'
        if os.path.exists(last_fp): os.remove(last_fp)

    # Langkah 2: scrape & append
    with open(file_path, 'a') as f:
        while current.date() <= yesterday.date():
            ds = current.strftime("%Y-%m-%d")
            current += timedelta(days=1)
            if ds in existing:
                continue
            prize = get_1st_prize(ds)
            if prize:
                f.write(f"{ds} {prize}\n")
                added.append(ds)

    # Langkah 3: base terkini
    updated = load_draws(file_path)
    if len(updated) >= 50:
        base_now = generate_base(updated, method='frequency', recent_n=50)
        save_base_to_file(base_now, 'data/base.txt')

    return f"✔️ {len(added)} draw baru ditambah." if added else "✔️ Tiada draw baru."
