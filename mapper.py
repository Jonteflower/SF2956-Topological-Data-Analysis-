import igraph as ig
import kmapper as km
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import sklearn
from sklearn.cluster import KMeans
from kmapper.cover import Cover

# Read the data
filepath = "formatted-data/footballData_averages_full.csv"
X = pd.read_csv(filepath)
X.dropna(inplace=True)

## Tweak these parameters
cluster = 2  # Number of clusters     to form using KMeans clustering algorithm.
category_to_group = 'points'  # Column name in the dataset used for color-coding and grouping data points in the visualization.
n_cubes = 32 # Number of intervals or "cubes" to divide the lens/projection into. Used in the cover of the topological space.
perc_overlap = 0.65  # Percentage of overlap between adjacent intervals/cubes in the cover. 
perplexity = 30  # Hyperparameter for t-SNE. Balances attention between local and global aspects of the data. Typically between 5 and 50.
learning_rate = 500  # Hyperparameter for t-SNE. Controls how much the projections adjust at each iteration. Common values range from 10 to 1000.

## Change columns examined here
selected_columns = [
    'Team',
    'Full Time Goals',
    'Half Time Goals',
    'Shots',
    'Shots on Target',
    'Corners',
    'Fouls Committed',
    'Yellow Cards',
    'Red Cards',
    'Average Win Odds',
    'Goals Conceded',
    'Shots Allowed',
    'Shots on Target Allowed',
    'Corners Allowed',
    'points',
    'wins',
    'draws',
    'losses'
]

# Filter the dataframe to select only the desired columns
existing_columns = [col for col in selected_columns if col in X.columns]
print("Dropped nan")
X_filtered = X[existing_columns].copy()

# Extract unique team names
names = X_filtered['Team'].values

# Drop non-numeric columns for further processing
X_filtered.drop(['Team'], axis=1, inplace=True)

# Get the overall averages for each stat for comparison later
means = np.mean(X_filtered.values, axis=0)
std_dev = np.std(X_filtered.values, axis=0)

# Initialise mapper and create lens using TSNE
mapper = km.KeplerMapper(verbose=0)

lens = mapper.fit_transform(
    X_filtered.values,
    # Tweaking the projecting can also create patterns
    projection=sklearn.manifold.TSNE(random_state=1234, perplexity=perplexity, learning_rate=learning_rate),
    #projection=PCA(n_components=2),

    scaler=None
)

# Create the graph of the nerve of the corresponding pullback
graph = mapper.map(
    lens,
    X_filtered.values,

    clusterer=KMeans(n_clusters=cluster, random_state=1234),
    cover=Cover(n_cubes=n_cubes, perc_overlap=perc_overlap)
)

def get_cluster_summary(player_list, average_mean, average_std, dataset, columns):
    # Compare teams against the average and list the attributes that are above and below the average
    cluster_mean = np.mean(dataset.iloc[player_list].values, axis=0)
    diff = cluster_mean - average_mean
    std_m = np.sqrt((cluster_mean - average_mean) ** 2) / average_std

    stats = sorted(zip(columns, cluster_mean, average_mean,
                       diff, std_m), key=lambda x: x[4], reverse=True)
    above_stats = [a[0] + ': ' + f'{a[1]:.2f}' for a in stats if a[3] > 0]
    below_stats = [a[0] + ': ' + f'{a[1]:.2f}' for a in stats if a[3] < 0]
    below_stats.reverse()

    # Create a string summary for the tooltips
    cluster_summary = 'Above Mean:<br>' + '<br>'.join(above_stats[:5]) + \
        '<br><br>Below Mean:<br>' + '<br>'.join(below_stats[-5:])
    return cluster_summary


def make_igraph_plot(graph, data, X, team_names, layout, mean_list, std_dev_list, title, line_color='rgb(136,136,136)'):
    div = '<br>-------<br>'
    node_list = []
    cluster_sizes = []
    avg_odds = []
    tooltip = []
    for node in graph['nodes']:
        node_list.append(node)
        teams = graph['nodes'][node]
        cluster_sizes.append(2 * int(np.log(len(teams) + 1) + 1))
        avg_odds.append(np.average([data.iloc[i][category_to_group]
                                    for i in teams]))
        node_info = node + div + '<br>'.join([team_names[i]
                                              for i in teams]) + div + get_cluster_summary(teams, mean_list, std_dev_list, X, X.columns)
        tooltip += tuple([node_info])

    # Add the edges to a list for passing into iGraph:
    edge_list = []
    for node in graph['links']:
        for nbr in graph['links'][node]:
            edge_list.append((node_list.index(node), node_list.index(nbr)))

    # Make the igraph plot
    g = ig.Graph(len(node_list))
    g.add_edges(edge_list)

    links = g.get_edgelist()
    plot_layout = g.layout(layout)

    n = len(plot_layout)
    x_nodes = [plot_layout[k][0] for k in range(n)]
    y_nodes = [plot_layout[k][1] for k in range(n)]

    x_edges = []
    y_edges = []
    for e in links:
        x_edges.extend([plot_layout[e[0]][0], plot_layout[e[1]][0], None])
        y_edges.extend([plot_layout[e[0]][1], plot_layout[e[1]][1], None])

    edges_trace = dict(type='scatter', x=x_edges, y=y_edges, mode='lines',
                       line=dict(color=line_color, width=0.3), hoverinfo='none')
    nodes_trace = dict(
        type='scatter',
        x=x_nodes,
        y=y_nodes,
        mode='markers',
        opacity=0.9,
        marker=dict(
            symbol='circle-dot',
            colorscale='Viridis',
            showscale=True,
            reversescale=False,
            color=avg_odds,
            size=cluster_sizes,
            line=dict(color=line_color, width=0.5),
            colorbar=dict(
                thickness=15,
                title=category_to_group,
                xanchor='left',
                titlefont=dict(color='white'),
                tickfont=dict(color='white')
            )
        ),
        text=tooltip,
        hoverinfo='text',
        textfont=dict(color='white')
    )

    fig = go.Figure(data=[edges_trace, nodes_trace])
    fig.update_layout(title=title, showlegend=False, hovermode='closest',
                      margin=dict(b=0, l=0, r=0, t=40),
                      xaxis=dict(showgrid=False, zeroline=False,
                                 showticklabels=False),
                      yaxis=dict(showgrid=False, zeroline=False,
                                 showticklabels=False),
                      annotations=[
                          dict(
                              showarrow=False,
                              xref="paper", yref="paper",
                              x=0.005, y=-0.002)
                      ]
                      )
    return fig

## Filter out nodes that have duplicate teams creating odd clusterings
def remove_duplicates_and_empty_clusters(graph):
    seen_teams = set()
    nodes_to_remove = []
    
    for node in graph['nodes']:
        unique_teams = []
        for team_index in graph['nodes'][node]:
            team_name = names[team_index]
            if team_name not in seen_teams:
                unique_teams.append(team_index)
                seen_teams.add(team_name)
                
        graph['nodes'][node] = unique_teams
        
        # If after processing, a node is empty, mark it for removal
        if not unique_teams:
            nodes_to_remove.append(node)
    
    # Remove the empty nodes from the graph
    for node in nodes_to_remove:
        del graph['nodes'][node]
        
        # Also remove any links associated with this node
        if node in graph['links']:
            del graph['links'][node]
        for _, links in graph['links'].items():
            if node in links:
                links.remove(node)
                
    return graph

graph = remove_duplicates_and_empty_clusters(graph)

title = 'Football Teams visualization with Mapper'
layout = 'fr'
fig = make_igraph_plot(graph, X, X_filtered, names,
                       layout, means, std_dev, title, )
fig.update_layout(title=title, showlegend=False, hovermode='closest',
                  margin=dict(b=0, l=0, r=0, t=40),
                  xaxis=dict(showgrid=False, zeroline=False,
                             showticklabels=False),
                  yaxis=dict(showgrid=False, zeroline=False,
                             showticklabels=False),
                  plot_bgcolor='rgba(20,20,20, 0.8)',
                  paper_bgcolor='rgba(20,20,20, 0.8)',
                  annotations=[
                      dict(
                          showarrow=False,
                          xref="paper", yref="paper",
                          x=0.005, y=-0.002)
                  ]
                  )
# Display the plot
fig.show()
