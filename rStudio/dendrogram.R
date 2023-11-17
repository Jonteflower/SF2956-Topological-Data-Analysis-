library(TDA)
library(dplyr)
library(readr)

# Load the dataset
data <- read_csv("footballData_2018_full.csv")
x_label <- "Teams 2018 Full Season"
# Compute average statistics for each team
team_stats <- data %>%
  group_by(Team) %>%
  summarise(
    `Full Time Goals` = mean(`Full Time Goals`, na.rm = TRUE),
    `Half Time Goals` = mean(`Half Time Goals`, na.rm = TRUE),
    Shots = mean(Shots, na.rm = TRUE),
    `Shots on Target` = mean(`Shots on Target`, na.rm = TRUE),
    Corners = mean(Corners, na.rm = TRUE),
    `Fouls Committed` = mean(`Fouls Committed`, na.rm = TRUE),
    `Yellow Cards` = mean(`Yellow Cards`, na.rm = TRUE),
    `Red Cards` = mean(`Red Cards`, na.rm = TRUE),
    `Shots on Target Allowed` = mean(`Shots on Target Allowed`, na.rm = TRUE),
    #points = mean(points, na.rm = TRUE),
    #wins = mean(wins, na.rm = TRUE),
    #draws = mean(draws, na.rm = TRUE),
    #losses = mean(losses, na.rm = TRUE)
    #`Average Win Odds` = mean(`Average Win Odds`, na.rm = TRUE),
    
  )

# Remove NAs
team_stats <- na.omit(team_stats)

# Ensure the matrix is numerical before computing the Vietoris-Rips diagram
team_matrix <- as.matrix(team_stats[, -1])

# Compute the Vietoris-Rips diagram
max_dimension <- 2
threshold <- 2
diagram <- ripsDiag(X = team_matrix, max_dimension, threshold, dist = "euclidean",
                    library = "GUDHI", location = FALSE, printProgress = FALSE)             

# Compute distance matrix and hierarchical clustering
dist_matrix <- dist(team_matrix)
hc1 <- hclust(dist_matrix, method = "single")
hc2 <- hclust(dist_matrix, method = "complete")
hc3 <- hclust(dist_matrix, method = "average")

# Compute the Vietoris-Rips diagram
max_dimension <- 2
threshold <- 2
diagram <- ripsDiag(X = team_matrix, max_dimension, threshold, dist = "euclidean",
                    library = "GUDHI", location = FALSE, printProgress = FALSE)

# Plot the persistence diagram
plot.diagram(diagram, barcode = FALSE)

# Set up a 1x3 plotting layout
par(mfrow=c(1,3))
par(mar=c(5.1, 4.1, 4.1, 2.1))

# Plot dendrograms
plot(hc1, labels = team_stats$Team, main = "Single Linkage Dendrogram", xlab = x_label, ylab = "Euclidean Distance")
plot(hc2, labels = team_stats$Team, main = "Complete Linkage Dendrogram", xlab = x_label, ylab = "Euclidean Distance")
plot(hc3, labels = team_stats$Team, main = "Average Linkage Dendrogram", xlab = x_label, ylab = "Euclidean Distance")



