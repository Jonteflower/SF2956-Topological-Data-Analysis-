import pandas as pd

def filter_by_year(input_file, output_file, year):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(input_file)

    # Filter rows that contain the given year in the "Team" column
    df_filtered = df[df['Team'].str.contains(str(year))]

    # Save the filtered DataFrame to a new CSV file
    df_filtered.to_csv(output_file, index=False)
    print(f"Data for the year {year} has been saved to {output_file}.")


def generate_year_data(year_to_extract, fileName):  
    output_filename = f"rStudio/footballData_{year_to_extract}.csv"
    filter_by_year(fileName, output_filename, year_to_extract)
    