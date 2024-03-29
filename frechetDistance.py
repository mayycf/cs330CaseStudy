import math
import csv
import matplotlib.pyplot as plt

# input: array of 2 tuples, [(x1, y1), (x2, y2)]
# output: returns the distance between them
def compute_distance(pts):
    return math.sqrt(((pts[0][0] - pts[1][0])*(pts[0][0] - pts[1][0])) + ((pts[0][1] - pts[1][1])*(pts[0][1] - pts[1][1])))

# finds the frechet distance between two trajectories
# output: returns a tuple of (frechet distance, DP matrix)
def fd(seriesA: list[(int, int)], seriesB: list[(int, int)]):
    lengthA = len(seriesA)
    lengthB = len(seriesB)
    matrix = [ [0]*(lengthB + 1) for i in range(lengthA + 1) ]
    for i in range(lengthA + 1):
        for j in range(lengthB + 1):
            matrix[i][j] = 10000000
    matrix[0][0] = 0
    for i in range(1, lengthA + 1):
        for j in range(1, lengthB + 1):
            dist = compute_distance([seriesA[i-1], seriesB[j-1]])
            minimum = min(matrix[i-1][j], matrix[i][j-1], matrix[i-1][j-1])
            matrix[i][j] = max(dist, minimum)
    return matrix[-1][-1], matrix

# finds the frechet distance assignment (i.e., how to pair points from the two trajectories)
# uses the dp matrix returned by fd()
def computeOptimalPath(matrix, seriesA, seriesB):
    histogram_input = []
    assignment = []
    n = len(matrix) - 1
    m = len(matrix[0]) - 1
    lastPoint = [seriesA[-1], seriesB[-1]]
    assignment.append(lastPoint)
    histogram_input.append(compute_distance(lastPoint))
    while n > 1 or m > 1:
        if n == 0:
            point = [seriesA[0], seriesB[m-2]]
            m -= 1
        elif m == 0:
            point = [seriesA[n-2], seriesB[0]]
            n -= 1
        else:
            minimum = min(matrix[n-1][m-1], matrix[n-1][m], matrix[n][m-1])
            if minimum == matrix[n-1][m-1]:
                point = [seriesA[n-2], seriesB[m-2]]
                n -= 1
                m -= 1
            elif minimum == matrix[n-1][m]:
                point = [seriesA[n-2], seriesB[m-1]]
                n -= 1
            else:
                point = [seriesA[n-1], seriesB[m-2]]
                m -= 1
        assignment.append(point)
        histogram_input.append(compute_distance(point))
    assignment.reverse()
    return assignment, histogram_input

# to parse file
def getPoints(file, x):
    points = []
    with open(file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if(row['id_'] == x):
                points.append([float(row["x"]), float(row["y"])])
    return points

# create histogram
def createHist(trajOne, trajTwo):
        nbins = 20
        distance, matrix = fd(trajOne, trajTwo)
        path, histogram_input = computeOptimalPath(matrix, trajOne, trajTwo)
        print(distance)
        print(len(histogram_input))
        plt.hist(histogram_input, edgecolor = 'white', linewidth = 1.2)
        plt.style.use('ggplot')
        plt.title(r'$E_{max}$ (Frechet Distance)')
        plt.xlabel('Edge Lengths')
        plt.ylabel('Frequency')
        plt.show()

if __name__ == "__main__" : 
    # trajectory inputs
    traj1 = getPoints('./geolife-cars.csv', '128-20080503104400')
    traj2 = getPoints('./geolife-cars.csv', '128-20080509135846')
    traj3 = getPoints('./geolife-cars.csv', '010-20081016113953')
    traj4 = getPoints('./geolife-cars.csv', '010-20080923124453')
    traj5 = getPoints('./geolife-cars.csv', '115-20080520225850')
    traj6 = getPoints('./geolife-cars.csv', '115-20080615225707')

    ### Frechet trajectory pair histograms ###
    createHist(traj1, traj2)
    # createHist(traj3, traj4)
    # createHist(traj5, traj6)