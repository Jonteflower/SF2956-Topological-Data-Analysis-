import csv
import re

# A dictionary mapping full team names
team_name_mapping = {
    'Blackpool': 'Blackpool',
    'Swansea City': 'Swansea',
    'Fulham': 'Fulham',
    'Birmingham': 'Birmingham',
    'Huddersfield Town': 'Huddersfield',
    'West Bromwich Albion': 'West Brom',
    'West Ham United': 'West Ham',
    'Norwich City': 'Norwich',
    'Aston Villa': 'Aston Villa',
    'Crystal Palace': 'Crystal Palace',
    'Blackburn Rovers': 'Blackburn',
    'Sunderland': 'Sunderland',
    'Burnley': 'Burnley',
    'Stoke City': 'Stoke',
    'Manchester City': 'Man City',
    'Wolverhampton Wanderers': 'Wolves',
    'Southampton': 'Southampton',
    'Portsmouth': 'Portsmouth',
    'Chelsea': 'Chelsea',
    'Watford': 'Watford',
    'Brentford': 'Brentford',
    'Sheffield United': 'Sheffield United',
    'Queens Park Rangers': 'QPR',
    'Bolton Wanderers': 'Bolton',
    'Leicester City': 'Leicester',
    'Brighton & Hove Albion': 'Brighton',
    'Leeds United': 'Leeds',
    'Liverpool': 'Liverpool',
    'Reading': 'Reading',
    'Newcastle United': 'Newcastle',
    'Nottingham Forest': "Nott'm Forest",
    'Cardiff City': 'Cardiff',
    'Hull City': 'Hull',
    'Manchester United': 'Man United',
    'Tottenham Hotspur': 'Tottenham',
    'Everton': 'Everton',
    'AFC Bournemouth': 'Bournemouth',
    'Arsenal': 'Arsenal',
    'Wigan Athletic': 'Wigan',
    'Middlesbrough': 'Middlesbrough'
}

team_names_second_format = ['Wolves', 'Tottenham', 'Sheffield United', 'Swansea', 'Sunderland', 'Hull', 'Norwich', 'West Ham', 'Southampton', 'Burnley', 'Portsmouth', 'QPR', 'Man United', 'Liverpool', 'Newcastle', 'West Brom', 'Crystal Palace', 'Middlesbrough', 'Everton', 'Fulham', 'Bournemouth', 'Birmingham', 'Aston Villa', "Nott'm Forest", 'Chelsea', 'Leicester', 'Watford', 'Leeds', 'Brentford', 'Reading', 'Brighton', 'Bolton', 'Arsenal', 'Huddersfield', 'Blackpool', 'Man City', 'Stoke', 'Blackburn', 'Cardiff', 'Wigan']

def format_names():
    # Update the team names in the CSV rows
    def update_team_names_in_csv(rows):
        updated_rows = []
        for row in rows:
            # Extracting team name before '-'
            team_with_year = row[1]
            team_name_parts = team_with_year.split('-')
            
            # Only process rows with the expected format
            if len(team_name_parts) != 2:
                print(f"Unexpected format for team_with_year: {team_with_year}")
                updated_rows.append(row)
                continue

            team_name, year = team_name_parts
            if team_name in team_name_mapping:
                # Replace with the shorter version and retain the year
                row[1] = team_name_mapping[team_name] + '-' + year
            
            updated_rows.append(row)
        return updated_rows

    # Read the CSV file
    with open("formatted-data/premier_league_standings.csv", "r") as file:
        reader = csv.reader(file)
        header = next(reader)  
        rows = list(reader) 

    # Call the function to update team names in the CSV rows
    updated_rows = update_team_names_in_csv(rows)

    # Write the formatted names back to the CSV file
    with open("formatted-data/premier_league_standings.csv", "w", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header) 
        writer.writerows(updated_rows)  

