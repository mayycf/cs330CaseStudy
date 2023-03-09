import csv, math
import queue, heapq
import matplotlib.pyplot as plt
import time

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
        # self.matrix[x][y] = 0
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
            hubList.append(cell)
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
    hubsList = hub_full.hubs(40, 2)
    print(hubsList)
    # print out end time - start time

    # test values: k = 10, r = 8km
    # hub_ten = Hub(ten_pts, 0.25)
    # hub_ten.densityPre()
    # hubsList = hub_ten.hubs(10, 8)
    # print(hubsList)

    # test values: k = 10, r = 8km
    # hub_thirty = Hub(thirty_pts, 0.25)
    # hub_thirty.densityPre()
    # hubsList = hub_thirty.hubs(10, 8)
    # print(hubsList)

    # test values: k = 10, r = 8km
    # hub_sixty = Hub(sixty_pts, 0.177)
    # hub_sixty.densityPre()
    # hubsList = hub_sixty.hubs(10, 8)
    # print(hubsList)

    ### PLOTTING ###
    # plt.scatter([item[0] for item in full_pts], [item[1] for item in full_pts], c = "blue", s = 0.01, alpha = 0.5, label = 'Points of $\mathscr{P}$')
    # plt.scatter([hub[0] for hub in hubsList], [hub[1] for hub in hubsList], c = 'red', s = 10, alpha = 0.75, label = 'Hubs identified (H)')
    # ax = plt.gca()
    # ax.set(xlim=(-75, 75))
    # for hub in hubsList:
    #     circle = plt.Circle((hub[0], hub[1]), radius = 8, color = 'black', linestyle='--', alpha = 0.9, fill = False)
    #     ax.add_artist(circle)
    # plt.legend(loc='upper right')
    # plt.title('Identifying Hubs in Geolife Cars')
    # plt.xlabel('Longitude (km)')
    # plt.ylabel('Latitude (km)')
    # plt.show()