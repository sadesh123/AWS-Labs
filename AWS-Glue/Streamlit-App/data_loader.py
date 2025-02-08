import pandas as pd
import streamlit as st


@st.cache_data
def load_data():
    # Load CSV files
    shot_density_df = pd.read_csv(r"C:\Path\To\Your\dataset.csv")
    shot_accuracy_df = pd.read_csv(r"C:\Path\To\Your\dataset.csv")
    top_shots_df = pd.read_csv(r"C:\Path\To\Your\dataset.csv")
    shot_location_df = pd.read_csv(r"C:\Path\To\Your\dataset.csv")

    return shot_density_df, shot_accuracy_df, top_shots_df, shot_location_df
