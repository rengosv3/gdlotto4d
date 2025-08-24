import os
import requests
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from bs4 import BeautifulSoup

from utils import load_draws, save_base_to_file
from strategies import generate_base

def get_1st_prize(date_str: str) -> str | None:
    url = f"https://gdlotto.net/results/ajax/_result.aspx?past=1&d={date_str}"
    try:
        resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        if resp.status_code != 200:
            return None
        soup = BeautifulSoup(resp.text, "html.parser")
        prize_tag = soup.find("span", id="1stPz")
        txt = prize_tag.text.strip() if prize_tag else ""
        if txt.isdigit() and len(txt) == 4:
            return txt
    except:
        pass
    return None

def update_draws(file_path: str = 'data/draws.txt', max_days_back: int = 181) -> str:
    from utils import save_base_to_file
    from strategies import generate_base

    strategies = ['frequency', 'hybrid', 'break', 'smartpattern', 'polarity_shift', 'hitfq']
    draws = load_draws(file_path)
    existing = {d['date'] for d in draws}

    tz = ZoneInfo("Asia/Kuala_Lumpur")
    now_my = datetime.now(tz)
    cutoff_hour = 20
    latest_date = now_my.date() if now_my.hour >= cutoff_hour else (now_my - timedelta(days=1)).date()

    if draws:
        last_date = datetime.strptime(draws[-1]['date'], "%Y-%m-%d").date()
    else:
        last_date = (now_my - timedelta(days=max_days_back)).date()

    current = last_date + timedelta(days=1)
    added = []
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, 'a') as f:
        while current <= latest_date:
            ds = current.strftime("%Y-%m-%d")
            current += timedelta(days=1)
            if ds in existing:
                continue
            prize = get_1st_prize(ds)
            if prize:
                f.write(f"{ds} {prize}\n")
                added.append(ds)

    # Load semula draw selepas kemas kini
    draws = load_draws(file_path)

    # Pastikan cukup draw
    if len(draws) < 51:
        return "❌ Tak cukup draw (minima 51)."

    # Tetapkan indeks
    current_draw = draws[-1]
    last_draw = draws[-2]

    # Padam & jana semula semua fail base
    base_dir = 'data'
    os.makedirs(base_dir, exist_ok=True)

    base_now = generate_base(draws, method='break', recent_n=50)
    base_last = generate_base(draws[:-1], method='break', recent_n=51)
    save_base_to_file(base_now, f"{base_dir}/base.txt")
    save_base_to_file(base_last, f"{base_dir}/base_last.txt")

    for method in strategies:
        base_now = generate_base(draws, method=method, recent_n=50)
        base_last = generate_base(draws[:-1], method=method, recent_n=51)
        save_base_to_file(base_now, f"{base_dir}/base_{method}.txt")
        save_base_to_file(base_last, f"{base_dir}/base_last_{method}.txt")

    return f"✔️ Update selesai. {'+{} draw baru'.format(len(added)) if added else 'Tiada draw baru'}."