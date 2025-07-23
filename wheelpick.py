# wheelpick.py

import itertools
from collections import Counter

def parse_manual_base(input_list):
    """
    Terima senarai 4 string dari input manual base.
    Setiap satu mestilah 5 digit tunggal, pisah dengan ruang.
    Contoh input_list: ['1 2 3 4 5', '0 1 2 3 4', '5 6 7 8 9', '0 2 4 6 8']
    Pulang: [['1','2','3','4','5'], ...] 
    Raise ValueError jika format tidak sah.
    """
    if len(input_list) != 4:
        raise ValueError("Perlu tepat 4 baris input untuk base.")
    base = []
    for line in input_list:
        digits = line.strip().split()
        if len(digits) != 5 or not all(d.isdigit() and len(d) == 1 for d in digits):
            raise ValueError("Setiap baris mesti ada tepat 5 digit tunggal (pisahkan dengan ruang).")
        base.append(digits)
    return base

def get_like_dislike_digits(draws, recent_n=30):
    """
    Dari `draws` (list of {'date','number'}) ambil top-3 paling kerap (like)
    dan bottom-3 paling jarang (dislike) dari `recent_n` terakhir.
    """
    recent = [d['number'] for d in draws[-recent_n:] if 'number' in d and len(d['number']) == 4]
    cnt = Counter()
    for num in recent:
        cnt.update(num)
    most = [d for d, _ in cnt.most_common(3)]
    least = [d for d, _ in cnt.most_common()[-3:]] if len(cnt) >= 3 else []
    return most, least

def generate_wheel_combos(base, lot="0.10"):
    """
    Dari `base` (list of 4 lists), hasilkan semua kombinasi
    dalam format "<num>#####<lot>".
    """
    combos = []
    for digits in itertools.product(*base):
        num = ''.join(digits)
        combos.append(f"{num}#####{lot}")
    return combos

def filter_wheel_combos(
    combos, draws,
    no_repeat=False,      # buang digit berulang
    no_triple=False,      # buang ada triple
    no_pair=False,        # buang ada pair
    no_ascend=False,      # buang menaik
    use_history=False,    # buang yang pernah keluar
    sim_limit=4,          # max sama posisi dengan last draw
    likes=None,           # wajib ada sekurang-kurangnya satu digit ini
    dislikes=None         # buang kalau ada digit ini
):
    """
    Tapis `combos` (list of "NNNN#####lot") mengikut kriteria.
    `draws` adalah history untuk sebarang penapisan.
    `likes`/`dislikes` adalah list digit (strings).
    `sim_limit`: max persamaan posisi dgn draw terakhir.
    """
    past = {d['number'] for d in draws}
    last = draws[-1]['number'] if draws else "0000"
    out = []
    likes = likes or []
    dislikes = dislikes or []

    for entry in combos:
        num, _ = entry.split("#####")
        digs = list(num)

        # 1) Tiada digit berulang
        if no_repeat and len(set(digs)) < 4:
            continue
        # 2) Tiada triple
        if no_triple and any(digs.count(d) >= 3 for d in set(digs)):
            continue
        # 3) Tiada pair
        if no_pair and any(digs.count(d) == 2 for d in set(digs)):
            continue
        # 4) Elak kombinasi menaik penuh
        if no_ascend and num in ["0123","1234","2345","3456","4567","5678","6789"]:
            continue
        # 5) Elak yang pernah keluar
        if use_history and num in past:
            continue
        # 6) Batas similarity dgn last draw
        sim = sum(1 for a, b in zip(num, last) if a == b)
        if sim > sim_limit:
            continue
        # 7) Like: perlu ada sekurang-kurangnya satu digit
        if likes and not any(d in likes for d in digs):
            continue
        # 8) Dislike: tiada digit terlarang
        if dislikes and any(d in dislikes for d in digs):
            continue

        out.append(entry)
    return out