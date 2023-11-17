from format_averages import format_averages
from format_names import format_names
from format_tables import format_tables
from scrape_data import scrape_data
from format_r_file import generate_year_data

def formatData():
    # Scrape the data
    #scrape_data()
        
    # Format the scraped data to match the formatting of the averages from hardcoded map
    format_names()

    # Averages depends in the names
    format_averages()

    # Do the tables last since tthey depend on the averages
    format_tables()

#formatData()

# Generate a yearly file for seasons toexamine further
year_to_generate = 2018
full_season = "formatted-data/footballData_averages_full.csv"
first_half = "formatted-data/footballData_averages_firstHalf.csv"
second_half = "formatted-data/footballData_averages_secondHalf.csv"

generate_year_data(year_to_generate, second_half)