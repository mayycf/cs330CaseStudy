### Algorithm ###
# iterate through all the points, check if a point is within a certain cell
# in a matrix, keep track of how many points are in each cell > choose cell size
# use those matrix values to determine hubs

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

class Hub:
    # pts: trajectory points
    # r_n: neighborhood radius
    # matrix: cell count represents how many points within a grid
    def __init__(self, pts, r_n, matrix = None):
        self.pts = pts
        self.r_n = r_n
        self.matrix = matrix
        
# pre-processing
# for data set -> minimum = -103.532808, maximum = 96.237468 -> rounded up to 105
# root 2 by the radius, grid cell length will be about 0.35, 0.25 for radius
    def densityPre(self):
        factor = 1/(self.r_n * math.sqrt(2))
        bound = math.ceil(factor * 105)
        doubleBound = 2 * bound
        denseMatrix = [ [0]*doubleBound for i in range(doubleBound) ]
        for point in self.pts:
            x = math.floor(point[0] * factor) + bound - 1   
            y = math.floor(point[1] * factor) + bound - 1
            denseMatrix[x][y] += 1
        self.matrix = denseMatrix
        return

    def density(self, point):
        factor = 1/(self.r_n * math.sqrt(2))
        bound = math.ceil(factor * 105)
        x = math.floor(point[0] * factor) + bound - 1
        y = math.floor(point[1] * factor) + bound - 1
        count = self.matrix[x][y]
        self.matrix[x][y] = 0
        return count

    def hubs(self, k, radius):
        PQ = []
        for point in self.pts:
            dense = self.density(point)
            if dense > 0:
                # priority based on negative density in order to sort correctly!
                heapq.heappush(PQ, (-dense, point))
        numHubs = 0
        hubList = []
        while numHubs < k:
            neighbors, cell = heapq.heappop(PQ)
            hubList.append((cell[0], cell[1]))
            numHubs += 1
            # index for PQ
            i = 0
            while i < len(PQ):
                x = PQ[i][1][0]
                y = PQ[i][1][1]
                if compute_distance([(x, y), cell]) <= radius:
                    PQ.pop(i)
                else:
                    i = i + 1
            heapq.heapify(PQ)
        return hubList

if __name__ == "__main__" : 
    ### INPUT ###
    full_pts = getPoints('./geolife-cars.csv')
    # ten_pts = getPoints('./geolife-cars-ten-percent.csv')
    # thirty_pts = getPoints('./geolife-cars-thirty-percent.csv')
    # sixty_pts = getPoints('./geolife-cars-sixty-percent.csv')

    ### FIND DENSITY HUBS ###
    # test values: k = 5, 10, 20, 40 and r = 2km
    hub_full = Hub(full_pts, 0.25)
    hub_full.densityPre()
    hubsList = hub_full.hubs(10, 10)
    print(hubsList)

    # test values: k = 10, r = 8km
    # hub_ten = Hub(ten_pts, 0.177)
    # hub_ten.densityPre()
    # hubsList = hub_ten.hubs(10, 8)
    # print(hubsList)

    # test values: k = 10, r = 8km
    # hub_thirty = Hub(thirty_pts, 0.177)
    # hub_thirty.densityPre()
    # hubsList = hub_thirty.hubs(10, 8)
    # print(hubsList)

    # test values: k = 10, r = 8km
    # hub_sixty = Hub(sixty_pts, 0.177)
    # hub_sixty.densityPre()
    # hubsList = hub_sixty.hubs(10, 8)
    # print(hubsList)

    # PLOTTING
    # plt.scatter([item[0] for item in full_pts], [item[1] for item in full_pts], c = "blue", s = 0.01, alpha = 0.5)
    # plt.show()


### EXTRA ###
# print("previous: ", [(-9.0, 3.25), (7.25, 1.0), (20.75, 0.0), (-42.5, -0.25), (-1.25, 13.0), (-43.75, 22.25), (-33.75, 8.75), (10.25, -19.75), (56.5, 11.5), (-23.25, 4.0)])