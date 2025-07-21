import os
from collections import Counter

def save_base_to_file(base_digits, file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w') as f:
        for pick in base_digits:
            f.write(' '.join(pick) + '\n')

def load_base_from_file(file_path):
    if not os.path.exists(file_path):
        return []
    base = []
    with open(file_path, 'r') as f:
        for line in f:
            digits = line.strip().split()
            if digits:
                base.append(digits)
    return base

def display_base_as_text(file_path):
    if not os.path.exists(file_path):
        return "⚠️ Tiada fail dijumpai."
    lines = []
    with open(file_path, 'r') as f:
        for i, line in enumerate(f):
            digits = line.strip()
            if digits:
                lines.append(f"Pick {i+1}: {digits}")
    return '\n'.join(lines)

def score_digits(draws, recent_n=30):
    weights = [Counter() for _ in range(4)]
    for i, draw in enumerate(draws[-recent_n:]):
        for j, digit in enumerate(draw['number']):
            weights[j][digit] += recent_n - i
    base = []
    for pick in weights:
        base.append([digit for digit, _ in pick.most_common(5)])
    return base