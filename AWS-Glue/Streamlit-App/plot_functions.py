import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st


# Function to plot shot density (heatmap)
def plot_shot_density(df):
    df.columns = df.columns.str.lower()  # Convert column names to lowercase

    shot_density = df.groupby(['year', 'loc_x', 'loc_y']).size().reset_index(name='shot_count')
    selected_year = st.selectbox("Select Year", shot_density['year'].unique())
    year_data = shot_density[shot_density['year'] == selected_year]
    pivot_data = year_data.pivot_table(values='shot_count', index='loc_y', columns='loc_x', fill_value=0)

    # Plot using seaborn heatmap (Streamlit doesn't have a built-in heatmap)
    plt.figure(figsize=(12, 8))
    sns.heatmap(pivot_data, cmap='YlGnBu', annot=False, cbar_kws={'label': 'Shot Count'}, xticklabels=5, yticklabels=5)
    plt.title(f"Shot Density for Year {selected_year}")
    st.pyplot(plt)


# Function to plot shot accuracy by year (line chart)
def plot_shot_accuracy(df):
    # Ensure accuracy_percentage is correctly calculated if it's not already in the data
    if 'accuracy_percentage' not in df.columns:
        df['accuracy_percentage'] = (df['shots_made'] / df['total_shots']) * 100

    # Group by 'YEAR' and calculate the average accuracy percentage
    accuracy_by_year = df.groupby('YEAR')['accuracy_percentage'].mean().reset_index()

    # Group by 'YEAR' and 'TEAM_NAME' to calculate team-wise accuracy
    # (Assuming you have 'team_name' column in your data; if not, this part can be omitted)
    if 'team_name' in df.columns:
        accuracy_by_team = df.groupby(['YEAR', 'team_name'])['accuracy_percentage'].mean().reset_index()

        # Display team-wise accuracy by year
        st.subheader('Shot Accuracy by Year (Team Breakdown)')
        for team in accuracy_by_team['team_name'].unique():
            team_data = accuracy_by_team[accuracy_by_team['team_name'] == team]
            st.write(f"Accuracy Trend for {team}")

            # Display the Streamlit line chart
            st.line_chart(team_data.set_index('YEAR')['accuracy_percentage'])
            st.write(f"X Axis: Year")
            st.write(f"Y Axis: Accuracy Percentage (%)")
            st.write("-" * 50)

    # Display the overall accuracy by year
    st.subheader('Shot Accuracy by Year (Overall)')

    # Display the Streamlit line chart for overall accuracy
    st.line_chart(accuracy_by_year.set_index('YEAR')['accuracy_percentage'])

    # Add labels using Streamlit elements
    st.write("X Axis: Year")
    st.write("Y Axis: Accuracy Percentage (%)")
    st.write("-" * 50)


# Function to plot top shots made by player and zone (bar chart)
def plot_top_shot_made_by_player_and_zone(df):
    # Group the data by player and basic_zone, then calculate the total shots made
    shot_made_by_player_and_zone = df.groupby(['player_name', 'basic_zone'])['shots_made'].sum().reset_index()

    # Sort the data by shots made in descending order and get top 5
    top_shots_by_zone = shot_made_by_player_and_zone.sort_values(by='shots_made', ascending=False).head(5)

    # Plot the data using Streamlit's bar chart
    st.bar_chart(top_shots_by_zone.set_index('player_name')['shots_made'])


# Function to plot shot location by team (heatmap)
def plot_shot_location_by_team(df):
    team_shot_location = df.groupby(['team_name', 'loc_x', 'loc_y']).size().reset_index(name='shot_count')
    team_name = st.selectbox("Select Team", team_shot_location['team_name'].unique())
    team_data = team_shot_location[team_shot_location['team_name'] == team_name]
    pivot_data = team_data.pivot_table(values='shot_count', index='loc_y', columns='loc_x', fill_value=0)

    # Plot using seaborn heatmap (Streamlit doesn't have a built-in heatmap)
    plt.figure(figsize=(12, 8))
    sns.heatmap(pivot_data, cmap='Blues', annot=False, cbar_kws={'label': 'Shot Count'}, xticklabels=5, yticklabels=5)
    plt.title(f"Shot Location for Team {team_name}")
    plt.xlabel('X Coordinate (Court Location)')
    plt.ylabel('Y Coordinate (Court Location)')
    st.pyplot(plt)
