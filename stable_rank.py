import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import gudhi as gd

def stable_rank(persistence, t):
    return sum(1 for (dim, (b, d)) in persistence if b <= t < d)

def compute_stable_ranks(data, max_edge_length=4.1, num_points=100):
    # Specify the columns of interest
    columns_of_interest = ['Full Time Goals', 'Half Time Goals', 'Shots', 'Shots on Target', 
                           'Corners', 'Fouls Committed', 'Yellow Cards', 'Red Cards', 
                           'Shots on Target Allowed']

    # Filter the dataset to include only the columns of interest
    team_stats = data[columns_of_interest]

    # Replace NaNs with the mean of each column
    team_stats = team_stats.apply(lambda x: x.fillna(x.mean()), axis=0)

    # Convert to numpy array for gudhi
    team_matrix = team_stats.to_numpy()
    
    # Build Vietoris-Rips complex
    rc = gd.RipsComplex(points=team_matrix, max_edge_length=max_edge_length)
    st = rc.create_simplex_tree(max_dimension=2)
    diag = st.persistence()
    
    # Compute stable ranks
    t_values = np.linspace(0, max_edge_length, num_points)
    raw_stable_ranks = [stable_rank(diag, t) for t in t_values]
    
    # Normalize stable ranks by the number of points
    normalized_stable_ranks = [rank / float(len(team_stats)) for rank in raw_stable_ranks]
    
    return t_values, normalized_stable_ranks

# Load datasets
full_path = "formatted-data/footballData_averages_full.csv"
full_data = pd.read_csv(full_path)

path_2018 = "formatted-data/footballData_2018_full.csv"
data_2018_full = pd.read_csv(path_2018)

path_2018_first_half = "formatted-data/footballData_2018_firstHalf.csv"
data_2018_first_half = pd.read_csv(path_2018_first_half)

path_2018_second_half = "formatted-data/footballData_2018_secondHalf.csv"
data_2018_second_half = pd.read_csv(path_2018_second_half)

# Compute normalized stable ranks for each dataset
t_values_full, stable_ranks_full = compute_stable_ranks(full_data)
t_values_2018_full, stable_ranks_2018_full = compute_stable_ranks(data_2018_full)
t_values_2018_first_half, stable_ranks_2018_first_half = compute_stable_ranks(data_2018_first_half)
t_values_2018_second_half, stable_ranks_2018_second_half = compute_stable_ranks(data_2018_second_half)

# Set up the plots - 2x2 grid for individual plots
fig, axs = plt.subplots(2, 2, figsize=(30, 10))  # Adjust figsize as needed

# Plot for the full dataset
axs[0, 0].plot(t_values_full, stable_ranks_full, label="Full Dataset")
axs[0, 0].set_title("Normalized Stable Rank for Full Dataset")
axs[0, 0].set_xlabel("Scale")
axs[0, 0].set_ylabel("Normalized Stable rank")

# Plot for the 2018 full dataset
axs[0, 1].plot(t_values_2018_full, stable_ranks_2018_full, label="2018 Full Dataset", color='orange')
axs[0, 1].set_title("Normalized Stable Rank for 2018 Full Season")
axs[0, 1].set_xlabel("Scale")
axs[0, 1].set_ylabel("Normalized Stable rank")

# Plot for the 2018 first half dataset
axs[1, 0].plot(t_values_2018_first_half, stable_ranks_2018_first_half, label="2018 First Half", color='green')
axs[1, 0].set_title("Normalized Stable Rank for 2018 First Half")
axs[1, 0].set_xlabel("Scale")
axs[1, 0].set_ylabel("Normalized Stable rank")

# Plot for the 2018 second half dataset
axs[1, 1].plot(t_values_2018_second_half, stable_ranks_2018_second_half, label="2018 Second Half", color='red')
axs[1, 1].set_title("Normalized Stable Rank for 2018 Second Half")
axs[1, 1].set_xlabel("Scale")
axs[1, 1].set_ylabel("Normalized Stable rank")

# Now, create a combined plot with all datasets
plt.figure(figsize=(10, 5))  # New figure for combined plot
plt.plot(t_values_full, stable_ranks_full, label="Full Dataset")
plt.plot(t_values_2018_full, stable_ranks_2018_full, label="2018 Full Season", color='orange')
plt.plot(t_values_2018_first_half, stable_ranks_2018_first_half, label="2018 First Half", color='green')
plt.plot(t_values_2018_second_half, stable_ranks_2018_second_half, label="2018 Second Half", color='red')
plt.title("Combined Normalized Stable Ranks")
plt.xlabel("Scale")
plt.ylabel("Normalized Stable rank")
plt.legend()  # Add legend to combined plot
plt.show()
