# iterate through all the points, check if a point is within a certain cell
# in a matrix, keep track of how many points are in each cell > choose cell size
# use those matrix values to determine hubs
# organize grid within 0.25 cells, determine if points are in certain ranges based on cell
# max 50, min -50

# choose highest density one - O(N), number of grid cells
# while loop, candidate set of hubs - all grid cells
# slowly add hubs, select cell with maximum density
# eliminate the cells that are within r