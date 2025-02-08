import streamlit as st
from data_loader import load_data
from plot_functions import plot_shot_density, plot_shot_accuracy, plot_top_shot_made_by_player_and_zone, \
    plot_shot_location_by_team


def main():
    st.title("NBA Shot Data Analysis")

    # Load data
    shot_density_df, shot_accuracy_df, top_shots_df, shot_location_df = load_data()

    # Display Shot Density Heatmap
    st.header("Shot Density Heatmap")
    plot_shot_density(shot_density_df)

    # Display Shot Accuracy by Year
    st.header("Shot Accuracy by Year")
    plot_shot_accuracy(shot_accuracy_df)

    # Display Top 5 Shot Made by Player and Zone
    st.header("Top 5 Shot Made by Player and Zone")
    plot_top_shot_made_by_player_and_zone(top_shots_df)

    # Display Shot Location by Team
    st.header("Shot Location by Team")
    plot_shot_location_by_team(shot_location_df)


if __name__ == "__main__":
    main()
