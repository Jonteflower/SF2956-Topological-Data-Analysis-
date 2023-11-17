import pandas as pd
from tqdm import tqdm
import pandas as pd
from tqdm import tqdm

def compute_team_averages_for_year(file_path, year, half='full'):
    df = pd.read_csv(file_path)

    # Splitting the dataframe based on the desired half of the season
    if half == 'first':
        df = df.iloc[:df.shape[0]//2]
    elif half == 'second':
        df = df.iloc[df.shape[0]//2:]

    # Define the columns for the odds from different bookmakers for the same outcome
    all_home_win_odds = ['B365H', 'BSH', 'BWH', 'GBH', 'IWH',
                         'LBH', 'PSH', 'PH', 'SOH', 'SBH', 'SJH', 'SYH', 'VCH', 'WHH']
    all_draw_odds = ['B365D', 'BSD', 'BWD', 'GBD', 'IWD', 'LBD',
                     'PSD', 'PD', 'SOD', 'SBD', 'SJD', 'SYD', 'VCD', 'WHD']
    all_away_win_odds = ['B365A', 'BSA', 'BWA', 'GBA', 'IWA',
                         'LBA', 'PSA', 'PA', 'SOA', 'SBA', 'SJA', 'SYA', 'VCA', 'WHA']

    # Identify which odds columns are present in the current dataset
    home_win_odds = [col for col in all_home_win_odds if col in df.columns]
    draw_odds = [col for col in all_draw_odds if col in df.columns]
    away_win_odds = [col for col in all_away_win_odds if col in df.columns]

    # Create lists to store the split rows
    new_rows = []

    for _, row in tqdm(df.iterrows(), total=df.shape[0]):

        home_row = {
            'Team': f"{row['HomeTeam']}-{year}",
            'Full Time Goals': round(row['FTHG'], 3),
            'Half Time Goals': round(row['HTHG'], 3),
            'Shots': round(row['HS'], 3),
            'Shots on Target': round(row['HST'], 3),
            'Corners': round(row['HC'], 3),
            'Fouls Committed': round(row['HF'], 3),
            'Yellow Cards': round(row['HY'], 3),
            'Red Cards': round(row['HR'], 3),
            'Average Win Odds': round(row[home_win_odds].mean(), 3),
            'Average Draw Odds': round(row[draw_odds].mean(), 3),
            # Away team's shots on target
            'Shots on Target Allowed': round(row['AST'], 3)
        }

        away_row = {
            'Team': f"{row['AwayTeam']}-{year}",
            'Full Time Goals': round(row['FTAG'], 3),
            'Half Time Goals': round(row['HTAG'], 3),
            'Shots': round(row['AS'], 3),
            'Shots on Target': round(row['AST'], 3),
            'Corners': round(row['AC'], 3),
            'Fouls Committed': round(row['AF'], 3),
            'Yellow Cards': round(row['AY'], 3),
            'Red Cards': round(row['AR'], 3),
            'Average Win Odds': round(row[away_win_odds].mean(), 3),
            'Average Draw Odds': round(row[draw_odds].mean(), 3),
            # Away team's shots on target
            'Shots on Target Allowed': round(row['HST'], 3),
            # 'Average Home Win Odds': round(row[home_win_odds].mean(), 3),
            # 'Average Draw Odds': round(row[draw_odds].mean(), 3),
        }

        new_rows.append(home_row)
        new_rows.append(away_row)

    # Convert the new rows into a DataFrame
    new_df = pd.DataFrame(new_rows)

    # Group by team and compute averages for each metric
    average_df = new_df.groupby('Team').mean().reset_index()

    # Round the columns to 3 decimal places
    cols_to_round = ['Full Time Goals', 'Half Time Goals', 'Shots', 'Shots on Target', 'Corners',
                     'Fouls Committed', 'Yellow Cards', 'Red Cards',
                     'Average Win Odds', 'Average Draw Odds']

    for col in cols_to_round:
        average_df[col] = average_df[col].round(3)

    return average_df


# Loop through the years and aggregate results
def averageData():
    all_data = {
        'full': [],
        'first': [],
        'second': []
    }

    years = [2008, 2009, 2010, 2011, 2012, 2013, 2014,
             2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022]

    for year in years:
        file_path = f"data/footballData{year}.csv"

        # For full season
        year_data_full = compute_team_averages_for_year(file_path, year)
        all_data['full'].append(year_data_full)

        # For first half of the season
        year_data_first = compute_team_averages_for_year(
            file_path, year, 'first')
        all_data['first'].append(year_data_first)

        # For second half of the season
        year_data_second = compute_team_averages_for_year(
            file_path, year, 'second')
        all_data['second'].append(year_data_second)

    # Concatenate all years data and save to respective files
    final_df_full = pd.concat(all_data['full'], axis=0).reset_index(drop=True)
    final_df_full.to_csv("formatted-data/footballData_averages.csv", index=False)

    final_df_first = pd.concat(
        all_data['first'], axis=0).reset_index(drop=True)
    final_df_first.to_csv(
        "formatted-data/footballData_averages_firstHalf.csv", index=False)

    final_df_second = pd.concat(
        all_data['second'], axis=0).reset_index(drop=True)
    final_df_second.to_csv(
        "formatted-data/footballData_averages_secondHalf.csv", index=False)

    # Concatenate all years data
    final_df_full = pd.concat(all_data['full'], axis=0).reset_index(drop=True)
    final_df_first = pd.concat(all_data['first'], axis=0).reset_index(drop=True)
    final_df_second = pd.concat(all_data['second'], axis=0).reset_index(drop=True)


    # Save the concatenated data to a CSV file
    final_df_full.to_csv("formatted-data/footballData_averages_full.csv", index=False)
    final_df_first.to_csv("formatted-data/footballData_averages_firstHalf.csv", index=False)
    final_df_second.to_csv("formatted-data/footballData_averages_secondHalf.csv", index=False)

def update_averages_with_points():
    # 1. Read the existing datasets
    team_odds = pd.read_csv("formatted-data/footballData_averages_full.csv")
    team_positions = pd.read_csv("formatted-data/premier_league_standings.csv")

    # 2. Merge the two datasets based on team-year to add the points, wins, draws, and losses columns
    merged_data = pd.merge(team_odds, team_positions[[
                           'team', 'points', 'wins', 'draws', 'losses']], left_on="Team", right_on="team", how="left")

    # Drop the duplicate 'team' column
    merged_data.drop('team', axis=1, inplace=True)

    # 3. Save the updated data to the footballData_averages_full.csv file
    merged_data.to_csv("formatted-data/footballData_averages_full.csv", index=False)



def format_averages():
    averageData()
    update_averages_with_points()
