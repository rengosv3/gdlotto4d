import itertools
from utils import get_like_dislike_digits

def generate_wheel_combos(base, lot="0.10", arah="kiri"):
    if arah == "kanan":
        base = list(reversed(base))
    elif arah != "kiri":
        raise ValueError("arah mesti 'kiri' atau 'kanan'")

    combos = []
    for digits in itertools.product(*base):
        num = ''.join(digits)
        combos.append(f"{num}#####{lot}")
    return combos

def filter_wheel_combos(combos, draws, no_repeat=False, no_triple=False, no_pair=False,
                         no_ascend=False, use_history=False, sim_limit=4, likes=None, dislikes=None):
    from collections import Counter

    past = {d['number'] for d in draws}
    last = draws[-1]['number'] if draws else "0000"
    out = []
    likes = likes or []
    dislikes = dislikes or []

    for entry in combos:
        num, _ = entry.split("#####")
        digs = list(num)

        if no_repeat and len(set(digs)) < 4:
            continue
        if no_triple and any(digs.count(d) >= 3 for d in set(digs)):
            continue
        if no_pair and any(digs.count(d) == 2 for d in set(digs)):
            continue
        if no_ascend and num in ["0123", "1234", "2345", "3456", "4567", "5678", "6789"]:
            continue
        if use_history and num in past:
            continue
        sim = sum(1 for a, b in zip(num, last) if a == b)
        if sim > sim_limit:
            continue
        if likes and not any(d in likes for d in digs):
            continue
        if dislikes and any(d in dislikes for d in digs):
            continue

        out.append(entry)
    return out