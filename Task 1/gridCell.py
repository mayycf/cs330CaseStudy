import csv
import math

# to parse file
def getPoints(file):
    points = []
    # minimum = 0
    # maximum = 0
    with open(file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            points.append([float(row["x"]), float(row["y"])])
            # maximum = max(maximum, points[-1][0], points[-1][1])
            # minimum = min(minimum, points[-1][0], points[-1][1])
    return points

# should I standardize this? feed min and max as inputs?
# pre-processing
def densityMatrix(pts):
    denseMatrix = [ [0]*840 for i in range(840) ]
    for point in pts:
        x = math.floor(point[0] * 4) + 419   # add 419 because 0-indexed matrix
        y = math.floor(point[1] * 4) + 419
        denseMatrix[x][y] += 1
    return denseMatrix

# full data set: minimum = -103.532808, maximum = 96.237468
full_pts = getPoints('./geolife-cars.csv')

# mtrx = densityMatrix(full_pts)

# Algorithm
# iterate through all the points, check if a point is within a certain cell
# in a matrix, keep track of how many points are in each cell > choose cell size
# use those matrix values to determine hubs
# organize grid within 0.25 cells, determine if points are in certain ranges based on cell
# max 50, min -50

# choose highest density one - O(N), number of grid cells
# while loop, candidate set of hubs - all grid cells
# slowly add hubs, select cell with maximum density
# eliminate the cells that are within r
        
        
