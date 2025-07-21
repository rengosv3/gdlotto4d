from collections import defaultdict

def cross_pick_analysis(draws):
    pick_data = [defaultdict(int) for _ in range(4)]
    for draw in draws:
        for i, digit in enumerate(draw['number']):
            pick_data[i][digit] += 1
    lines = []
    for i, pd in enumerate(pick_data):
        common = sorted(pd.items(), key=lambda x: -x[1])[:5]
        lines.append(f"Pick {i+1}: {', '.join(f'{d} ({c}x)' for d, c in common)}")
    return '\n'.join(lines)