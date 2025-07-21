import streamlit as st
import os

SUPER_BASE_PATH = "data/base_super.txt"

def load_super_base():
    if os.path.exists(SUPER_BASE_PATH):
        with open(SUPER_BASE_PATH, "r") as f:
            lines = f.read().splitlines()
            return [line.strip() for line in lines if line.strip()]
    else:
        return []

def display_super_base():
    st.subheader("🌟 Super Base Digit Ranking")

    super_base = load_super_base()

    if not super_base:
        st.warning("Tiada data Super Base. Sila tambah fail `base_super.txt` di folder data/.")

    else:
        st.markdown("#### 📊 Ranking Digit (Super Base):")
        for idx, line in enumerate(super_base, start=1):
            st.markdown(f"**#{idx}:** {line}")

    st.info("Data ini digunakan untuk menilai kedudukan digit dari AI & Insight.")
