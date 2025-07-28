import streamlit as st
import itertools
from collections import Counter

from utils import load_draws, load_base_from_file
from strategies import generate_base

def get_like_dislike_digits(draws, recent_n=30):
    recent = [d['number'] for d in draws[-recent_n:] if 'number' in d and len(d['number']) == 4]
    cnt = Counter()
    for num in recent:
        cnt.update(num)
    most = [d for d, _ in cnt.most_common(3)]
    least = [d for d, _ in cnt.most_common()[-3:]] if len(cnt) >= 3 else []
    return most, least

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

def filter_wheel_combos(
    combos, draws,
    no_repeat=False, no_triple=False, no_pair=False, no_ascend=False,
    use_history=False, sim_limit=4, likes=None, dislikes=None
):
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
        if no_ascend and num in ["0123","1234","2345","3456","4567","5678","6789"]:
            continue
        if use_history and num in past:
            continue
        sim = sum(1 for a,b in zip(num, last) if a==b)
        if sim > sim_limit:
            continue
        if likes and not any(d in likes for d in digs):
            continue
        if dislikes and any(d in dislikes for d in digs):
            continue

        out.append(entry)
    return out

def show_wheelpick_tab(draws):
    st.header("🎡 Wheelpick Generator")

    # strategi sama seperti tab Ramalan
    strategies = ['frequency', 'polarity_shift', 'hybrid', 'break', 'smartpattern', 'hitfq']

    # arah & likes/dislikes
    arah_wp = st.radio("Arah:", ["Kiri→Kanan", "Kanan→Kiri"], key="wp_dir")
    like, dislike = get_like_dislike_digits(draws)
    st.markdown(f"👍 Like: `{like}`    👎 Dislike: `{dislike}`")
    user_like = st.text_input("Digit Like:", value=' '.join(like), key="wp_like")
    user_dislike = st.text_input("Digit Dislike:", value=' '.join(dislike), key="wp_dislike")
    likes = user_like.split()
    dislikes = user_dislike.split()

    # input base
    input_mode = st.radio("Input Base:", ["Auto dari strategi", "Manual"], key="wp_mode")
    if input_mode == "Auto dari strategi":
        strat_wp = st.selectbox("Strategi Base:", strategies, key="wp_strat")
        recent_wp = st.slider("Draw untuk base:", 5, len(draws), 30, 5, key="wp_n")
        try:
            base_wp = generate_base(draws, method=strat_wp, recent_n=recent_wp)
        except Exception as e:
            st.error(str(e))
            st.stop()
    else:
        manual_base = st.text_area("Masukkan Base Manual (4 baris, digit pisah space)", height=120, key="wp_manual")
        try:
            base_wp = [line.strip().split() for line in manual_base.strip().split('\n')]
            if len(base_wp) != 4 or any(not p for p in base_wp):
                raise ValueError("Format base tak sah.")
        except Exception as e:
            st.error(f"Base manual error: {e}")
            st.stop()

    lot = st.text_input("Nilai Lot:", value="0.10", key="wp_lot")

    with st.expander("⚙️ Tapisan Tambahan"):
        no_repeat = st.checkbox("Buang digit ulang", key="f1")
        no_triple = st.checkbox("Buang triple", key="f2")
        no_pair   = st.checkbox("Buang pair", key="f3")
        no_ascend = st.checkbox("Buang menaik", key="f4")
        use_history = st.checkbox("Buang pernah keluar", key="f5")
        sim_limit = st.slider("Max sama dgn last draw:", 0, 4, 2, key="f6")

    if st.button("🎰 Create Wheelpick", key="wp_run"):
        arah = "kiri" if arah_wp=="Kiri→Kanan" else "kanan"
        combos = generate_wheel_combos(base_wp, lot=lot, arah=arah)
        st.info(f"Sebelum tapis: {len(combos)}")
        filtered = filter_wheel_combos(
            combos, draws,
            no_repeat, no_triple, no_pair, no_ascend,
            use_history, sim_limit,
            likes, dislikes
        )
        st.success(f"Selepas tapis: {len(filtered)}")
        for i in range(0, len(filtered), 30):
            part = filtered[i:i+30]
            st.markdown(f"**Bahagian {(i//30)+1}:**")
            st.code('\n'.join(part), language='text')
        data = '\n'.join(filtered).encode()
        st.download_button("💾 Muat Turun", data=data,
                           file_name="wheelpick.txt", mime="text/plain")