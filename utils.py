import os
import json
from datetime import datetime, timedelta
from draw_scraper import scrape_latest_draws
from collections import Counter

DATA_DIR = "data"
DRAW_FILE = os.path.join(DATA_DIR, "draws.txt")
BASE_FILE = os.path.join(DATA_DIR, "base_today.txt")

def load_draws() -> list:
    if not os.path.exists(DRAW_FILE):
        return []
    with open(DRAW_FILE, "r") as f:
        return [json.loads(line.strip()) for line in f if line.strip()]

def save_draws(draws: list):
    with open(DRAW_FILE, "w") as f:
        for d in draws:
            f.write(json.dumps(d) + "\n")

def update_draws(n_days: int = 1):
    draws = load_draws()
    latest_date = draws[-1]["date"] if draws else "2000-01-01"
    new_draws = scrape_latest_draws(n_days, latest_date)
    if new_draws:
        draws.extend(new_draws)
        save_draws(draws)

def load_base_from_file() -> list[list[str]]:
    if not os.path.exists(BASE_FILE):
        return [[]] * 4
    with open(BASE_FILE, "r") as f:
        return json.load(f)

def save_base_to_file(base: list[list[str]]):
    with open(BASE_FILE, "w") as f:
        json.dump(base, f)

from strategies import generate_base

def update_base_today():
    draws = load_draws()
    base = generate_base(draws, method="hybrid")
    save_base_to_file(base)

def get_like_dislike_digits(draws, recent_n=30):
    recent = [d['number'] for d in draws[-recent_n:] if 'number' in d and len(d['number']) == 4]
    cnt = Counter()
    for num in recent:
        cnt.update(num)
    most = [d for d, _ in cnt.most_common(3)]
    least = [d for d, _ in cnt.most_common()[-3:]] if len(cnt) >= 3 else []
    return most, least