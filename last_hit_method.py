from collections import defaultdict

def last_hit_method(draws, recent_n):
    """
    Kira digit yang muncul dalam setiap posisi untuk N draw terkini.
    Pulangkan dict: posisi → senarai digit unik.
    """
    last_hit = defaultdict(set)
    for idx in range(-recent_n, 0):
        if idx + len(draws) < 0:
            continue
        number = str(draws[idx]['number']).zfill(4)
        for pos, digit in enumerate(number):
            last_hit[pos].add(int(digit))
    return {pos: list(digits) for pos, digits in last_hit.items()}