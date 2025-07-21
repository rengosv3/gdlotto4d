import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

def show_digit_heatmap(draws):
    df = pd.DataFrame([list(d['number']) for d in draws[-100:]], columns=["P1", "P2", "P3", "P4"])
    fig, ax = plt.subplots(figsize=(8, 4))
    sns.heatmap(df.apply(pd.Series.value_counts).fillna(0).T, annot=True, cmap="YlGnBu", ax=ax)
    st.pyplot(fig)

def show_digit_distribution(draws):
    df = pd.DataFrame([list(d['number']) for d in draws], columns=["P1", "P2", "P3", "P4"])
    fig, axs = plt.subplots(2, 2, figsize=(10, 6))
    axs = axs.flatten()
    for i in range(4):
        sns.countplot(x=df.iloc[:, i], ax=axs[i], palette="Set2")
        axs[i].set_title(f"Digit di Pick {i+1}")
    st.pyplot(fig)