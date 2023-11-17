import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_season_data(year):
    # Get the next year
    next_year = str((int(year) + 1) % 100).zfill(2)

    url = f"https://www.toffeeweb.com/season/{year}-{next_year}/premtable.php"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    table = soup.find('table', id='premtable')
    rows = table.find_all('tr')[1:]  # Skip header row

    season_data = []
    for row in rows:
        columns = row.find_all('td')
        placement = columns[0].text.strip()
        team = f"{columns[1].text.strip()}-20{year}"
        wins = columns[3].text.strip()
        draws = columns[4].text.strip()
        losses = columns[5].text.strip()
        points = (int(wins) * 3) + int(draws)  # Calculating points here
        season_data.append([placement, team, wins, draws, losses, str(points)])  # Convert points to string for consistency

    return season_data


def scrape_data():
    all_data = []
    for year in range(8, 23):  # For years 08-09 to 22-23
        year_str = str(year).zfill(2)
        all_data.extend(scrape_season_data(year_str))

    # Convert to DataFrame for easier manipulation
    df = pd.DataFrame(all_data, columns=[
                    'placement', 'team', 'wins', 'draws', 'losses', 'points'])
    print(df)

    df.to_csv('formatted-data/premier_league_standings.csv', index=False)
