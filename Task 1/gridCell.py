### Algorithm ###
# iterate through all the points, check if a point is within a certain cell
# in a matrix, keep track of how many points are in each cell > choose cell size
# use those matrix values to determine hubs
# organize grid within 0.25 cells, determine if points are in certain ranges based on cell

# choose highest density one - O(N), number of grid cells
# while loop, candidate set of hubs - all grid cells
# slowly add hubs, select cell with maximum density
# eliminate the cells that are within r

import csv, math
import queue, heapq
import matplotlib.pyplot as plt

# input: array of 2 tuples, [(x1, y1), (x2, y2)]
# output: returns the distance between the 2 points
def compute_distance(pts):
    return math.sqrt(((pts[0][0] - pts[1][0])*(pts[0][0] - pts[1][0])) + ((pts[0][1] - pts[1][1])*(pts[0][1] - pts[1][1])))

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
# root 2 by the radius, grid cell length will be about 0.35, 0.25 for radius
def densityMatrix(pts):
    denseMatrix = [ [0]*840 for i in range(840) ]
    for point in pts:
        x = math.floor(point[0] * 4) + 419   # add 419 because 0-indexed matrix
        y = math.floor(point[1] * 4) + 419
        denseMatrix[x][y] += 1
    return denseMatrix

def density(matrix, point):
    x = point[0]
    y = point[1]
    count = matrix[x][y]
    # if x > 0:
    #     count += matrix[x-1][y]
    #     if y < 839:
    #         count += matrix[x-1][y+1]
    #     if y > 0:
    #         count += matrix[x-1][y-1]
    # if x < 839:
    #     count += matrix[x+1][y]
    #     if y < 839:
    #         count += matrix[x+1][y+1]
    #     if y > 0:
    #         count += matrix[x+1][y-1]
    # if y < 839:
    #     count += matrix[x][y+1]
    # if y > 0:
    #     count += matrix[x][y-1]
    return count

def hubs(matrix, k, radius):
    PQ = []
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            dense = 0
            dense = density(matrix, [i, j])
            if dense != 0:
                # priority based on negative density in order to sort correctly!
                heapq.heappush(PQ, (-dense, [i, j]))
                
    numHubs = 0
    hubList = []
    while numHubs < k:
        neighbors, cell = heapq.heappop(PQ)
        
        # convert cell back to standard point
        xnorm = (cell[0] - 419)/4
        ynorm = (cell[1] - 419)/4
        # hubList.append([-neighbors, (xnorm, ynorm)])
        hubList.append((xnorm, ynorm))
        numHubs += 1
        
        # index
        i = 0
        
        while i < len(PQ):
            x = PQ[i][1][0]
            y = PQ[i][1][1]
            # if x >= xmin and x <= xmax and y >= ymin and y <= ymax:
            if compute_distance([(x, y), cell]) <= radius*4:
                PQ.pop(i)
            else:
                i = i + 1
        heapq.heapify(PQ)
    return hubList
    

### INPUT ###
full_pts = getPoints('./geolife-cars.csv') # minimum = -103.532808, maximum = 96.237468
# ten_pts, minimum, maximum = getPoints('./geolife-cars-ten-percent.csv')
# thirty_pts = getPoints('./geolife-cars-thirty-percent.csv')
# sixty_pts = getPoints('./geolife-cars-sixty-percent.csv')

### FIND DENSITY HUBS ###
# test values: k = 5, 10, 20, 40 and r = 2km
matrix = densityMatrix(full_pts)
hubsList = hubs(matrix, 40, 2)
print(hubsList)

# k = 10, r = 8km

# distances = []
# for i in range(len(hubsList)):
#     for j in range(len(hubsList)):
#         if i != j:
#             distances.append(compute_distance([hubsList[i], hubsList[j]]))
# print(min(distances))

# PLOTTING
# plt.scatter([item[0] for item in full_pts], [item[1] for item in full_pts], c = "blue", s = 0.01, alpha = 0.5)
# plt.show()
