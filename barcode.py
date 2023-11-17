import gudhi as gd
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.decomposition import PCA

# Function to load data and compute persistence diagram
def load_data_and_compute_persistence(path):
    data = pd.read_csv(path)

    # Specify the columns of interest
    columns_of_interest = ['Full Time Goals', 'Half Time Goals', 'Shots', 'Shots on Target', 
                           'Corners', 'Fouls Committed', 'Yellow Cards', 'Red Cards', 
                           'Shots on Target Allowed']

    # Filter the dataset to include only the columns of interest
    team_stats = data[columns_of_interest]

    # Replace NaNs with the mean of each column
    team_stats = team_stats.apply(lambda x: x.fillna(x.mean()), axis=0)

    # Apply PCA to reduce dimensions
    pca = PCA(n_components=2)  # Reduced to 2 for simplicity
    team_matrix_reduced = pca.fit_transform(team_stats)

    # Build Vietoris-Rips complex
    rc = gd.RipsComplex(points=team_matrix_reduced, max_edge_length=4.1)
    st = rc.create_simplex_tree(max_dimension=2)
    diag = st.persistence()
    
    return diag

# Function to plot persistence barcode and diagram
def plot_persistence(diag, fig, position, title):
    # Barcode plot
    ax = fig.add_subplot(1, 4, position)
    gd.plot_persistence_barcode(diag, axes=ax)
    ax.set_title(f"{title} Barcode")

    # Increase position for the persistence diagram
    position += 1
    ax = fig.add_subplot(1, 4, position)
    gd.plot_persistence_diagram(diag, axes=ax)
    ax.set_title(f"{title} Diagram")

# Load datasets
full_dataset_path = "formatted-data/footballData_averages_full.csv"
data_2018_path = "formatted-data/footballData_2018_full.csv"

# Compute persistence diagrams
full_diag = load_data_and_compute_persistence(full_dataset_path)
data_2018_diag = load_data_and_compute_persistence(data_2018_path)

# Plotting
fig = plt.figure(figsize=(24, 6))

# Plot persistence barcode and diagram for the full dataset
plot_persistence(full_diag, fig, 1, "Full Dataset")

# Plot persistence barcode and diagram for the 2018 dataset
plot_persistence(data_2018_diag, fig, 3, "2018 Dataset")

plt.tight_layout()
plt.show()
