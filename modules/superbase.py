from .base_analysis import score_digits

def generate_super_base(draws):
    base_30 = score_digits(draws, 30)
    base_60 = score_digits(draws, 60)
    base_120 = score_digits(draws, 120)
    super_base = []
    for i in range(4):
        common = set(base_30[i]) & set(base_60[i]) & set(base_120[i])
        combined = list(common) + [d for d in base_30[i] if d not in common]
        super_base.append(combined[:5])
    return super_base