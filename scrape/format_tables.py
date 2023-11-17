import pandas as pd

def format_tables():
    # 1. Read the existing datasets
    team_odds = pd.read_csv("formatted-data/footballData_averages.csv")
    team_positions = pd.read_csv("formatted-data/premier_league_standings.csv")
    
    # Rename points in team_positions to avoid conflict
    team_positions = team_positions.rename(columns={"points": "season_points"})

    # 2. Merge the two datasets based on team-year
    merged_data = pd.merge(team_positions, team_odds, left_on="team", right_on="Team")
    
    # 3. Group by placement and calculate average, median, and standard deviation for the win odds
    grouped_data_odds = merged_data.groupby("placement")["Average Win Odds"].agg(['mean', 'median', 'std'])

    # Round the columns to 2 decimal places
    grouped_data_odds = grouped_data_odds.round(2)

    # 4. Save the final aggregated data for win odds to a new CSV file
    grouped_data_odds.to_csv("formatted-data/table_avg_odds.csv")
    
    # Group by placement and calculate average, median, and standard deviation for the points
    grouped_data_points = merged_data.groupby("placement")["points"].agg(['mean', 'median', 'std'])

    # Round the columns to 2 decimal places
    grouped_data_points = grouped_data_points.round(2)

    # 5. Save the final aggregated data for points to a new CSV file
    grouped_data_points.to_csv("formatted-data/table_avg_points.csv")

