# prediction.py
import itertools

def generate_predictions_from_base(base, max_preds=10):
    """
    Dari `base` (list of 4 lists), hasilkan kombinasi 4D dalam format string.
    Pulangkan maksimum `max_preds` nombor teratas.
    """
    # Semua kombinasi cartesian
    combos = [''.join(p) for p in itertools.product(*base)]
    return combos[:max_preds]