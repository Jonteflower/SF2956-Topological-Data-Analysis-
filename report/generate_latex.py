import csv

def generate_latex_table_from_csv(file_path):
    with open(file_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        header = next(reader)
        
        # Start table environment and tabular environment
        latex_table = "\\begin{table}\n"
        latex_table += "\\centering\n"
        latex_table += "\\begin{tabular}{" + "c" * len(header) + "}\n"
        
        # Add header
        latex_table += " & ".join(header) + " \\\\\n"
        latex_table += "\\hline\n"
        
        # Add rows
        for row in reader:
            latex_table += " & ".join(row) + " \\\\\n"
        
        # End tabular and table environment
        latex_table += "\\end{tabular}\n"
        latex_table += "\\end{table}\n"
        
    return latex_table

avg_points_latex_table = generate_latex_table_from_csv('formatted-data/table_avg_points.csv')
avg_odds_latex_table = generate_latex_table_from_csv('formatted-data/table_avg_odds.csv')

with open('latex_tables_output.tex', 'w') as outfile:
    outfile.write(avg_points_latex_table)
    outfile.write("\n\n")
    outfile.write(avg_odds_latex_table)
