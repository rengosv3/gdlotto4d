import os
from collections import Counter, defaultdict
from datetime import datetime
from .base_analysis import score_digits, save_base_to_file, load_base_from_file

def get_last_result_insight(draws):
    if not draws:
        return "Tiada data draw tersedia."
    today_str = datetime.today().strftime("%Y-%m-%d")
    last_valid = next((d for d in reversed(draws) if d['date'] < today_str), None)
    if not last_valid:
        return "Tiada data draw semalam tersedia."

    last_number = last_valid['number']
    last_date = last_valid['date']
    insight_lines = [f"📅 Nombor terakhir naik: **{last_number}** pada {last_date}\n"]

    all_numbers = [d['number'] for d in draws if len(d['number']) == 4]
    digit_counter = [Counter() for _ in range(4)]
    for number in all_numbers:
        for i, digit in enumerate(number):
            digit_counter[i][digit] += 1

    base_path = 'data/base_last.txt'
    if not os.path.exists(base_path):
        base_digits = score_digits(draws[:-1])
        save_base_to_file(base_digits, base_path)
    base_digits = load_base_from_file(base_path)

    cross_data = [defaultdict(int) for _ in range(4)]
    for number in all_numbers:
        for i, digit in enumerate(number):
            cross_data[i][digit] += 1
    cross_top = [[d for d, _ in sorted(c.items(), key=lambda x: -x[1])[:5]] for c in cross_data]

    insight_lines.append("📋 **Base Digunakan:**")
    for i, pick in enumerate(base_digits):
        insight_lines.append(f"- Pick {i+1}: {' '.join(pick)}")
    insight_lines.append("")

    for i, digit in enumerate(last_number):
        freq = digit_counter[i][digit]
        rank = sorted(digit_counter[i].values(), reverse=True).index(freq) + 1
        in_base = "✅" if digit in base_digits[i] else "❌"
        in_cross = "✅" if digit in cross_top[i] else "❌"
        score = 0
        if rank <= 3: score += 2
        elif rank <= 5: score += 1
        if in_base == "✅": score += 2
        if in_cross == "✅": score += 1
        label = "🔥 Sangat berpotensi" if score >= 4 else "👍 Berpotensi" if score >= 3 else "❓ Kurang pasti"
        insight_lines.append(
            f"Pick {i+1}: Digit '{digit}' - Ranking #{rank}, Base: {in_base}, Cross: {in_cross} → **{label}**\n"
        )

    insight_lines.append("\n💡 AI Insight:")
    insight_lines.append("- Digit dalam Base & Cross berkemungkinan besar naik semula.")
    insight_lines.append("- Ranking tinggi (Top 3) menunjukkan konsistensi kuat.")
    return '\n'.join(insight_lines)