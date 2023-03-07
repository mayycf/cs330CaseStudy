import csv
import math
import queue, heapq
import matplotlib.pyplot as plt

# to parse file
def getPoints(file):
    points = []
    with open(file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            points.append([float(row["x"]), float(row["y"])])
    return points

# pre-processing
# minimum: -105, maximum: 105 -> 0.25 x 0.25 km grids represented by the matrix 
# minimum: -420, maximum: 420 -> n x m matrix where n = m = 840
def densityMatrix(pts):
    denseMatrix = [ [0]*840 for i in range(840) ]
    for point in pts:
        x = math.floor(point[0] * 4) + 419   # add 419 because 0-indexed matrix
        y = math.floor(point[1] * 4) + 419
        denseMatrix[x][y] += 1
    return denseMatrix

# not really a necessary function
def density(matrix, point):
    x = math.floor(point[0] * 4) + 419
    y = math.floor(point[1] * 4) + 419
    return matrix[x][y]

def hubs(matrix, k, radius):
    PQ = []
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] != 0:
                # priority based on negative density in order to sort correctly!
                heapq.heappush(PQ, (-matrix[i][j], [i, j]))
                
    numHubs = 0
    hubList = []
    while numHubs < k:
        density, cell = heapq.heappop(PQ)
        
        # convert cell back to standard point
        xnorm = (cell[0] - 419)/4
        ynorm = (cell[1] - 419)/4
        hubList.append([-density, (xnorm, ynorm)])
        numHubs += 1
        
        # calculate bounds
        xmin = cell[0] - (radius*4)
        xmax = cell[0] + (radius*4)
        ymin = cell[1] - (radius*4)
        ymax = cell[1] + (radius*4)
        
        # index
        i = 0
        while i < len(PQ):
            x = PQ[i][1][0]
            y = PQ[i][1][1]
            if x >= xmin and x <= xmax and y >= ymin and y <= ymax:
                PQ.pop(i)
            i = i + 1
        heapq.heapify(PQ)
    return hubList
    

### INPUT ###
full_pts = getPoints('./geolife-cars.csv') # minimum = -103.532808, maximum = 96.237468
# ten_pts, minimum, maximum = getPoints('./geolife-cars-ten-percent.csv')
# thirty_pts = getPoints('./geolife-cars-thirty-percent.csv')
# sixty_pts = getPoints('./geolife-cars-sixty-percent.csv')

matrix = densityMatrix(full_pts)
print(hubs(matrix, 10, 10))

# PLOTTING
# plt.scatter([item[0] for item in full_pts], [item[1] for item in full_pts], c = "blue", s = 0.01)
# plt.show()

# def density(point, matrix, radius):
#     x = math.floor(point[0] * 4) + 419
#     y = math.floor(point[1] * 4) + 419
#     xmin = (x - radius) * 4
#     xmax = (x + radius) * 4
#     ymin = (y - radius) * 4
#     ymax = (y + radius) * 4
#     count = 0
#     for i in range(xmin, xmax):
#         for j in range(ymin, ymax):
#             if compute_distance([[i, j], point])
#     return matrix[x][y]

# x, y = p
#     xmin = max(0, x - radius)
#     xmax = min(matrix.shape[0], x + radius + 1)
#     ymin = max(0, y - radius)
#     ymax = min(matrix.shape[1], y + radius + 1)

#     count = 0
#     for i in range(xmin, xmax):
#         for j in range(ymin, ymax):
#             if ((i - x) ** 2 + (j - y) ** 2) ** 0.5 <= radius:
#                 count += matrix[i, j]

#     area = (2 * radius + 1) ** 2
#     return count / area

# matrix = densityMatrix(full_pts)
# print(matrix)

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
        
        
