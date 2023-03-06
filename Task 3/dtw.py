# NEED TO CHANGE, DIFFERENT FROM ASSIGNMENT 4
import math
import csv

# input: array of 2 tuples, [(x1, y1), (x2, y2)]
# output: returns the distance between the 2 points
def compute_distance(pts):
    return math.sqrt(((pts[0][0] - pts[1][0])*(pts[0][0] - pts[1][0])) + ((pts[0][1] - pts[1][1])*(pts[0][1] - pts[1][1])))

def dtw(seriesA: list[(int, int)], seriesB: list[(int, int)]):
    lengthA = len(seriesA)
    lengthB = len(seriesB)
    matrix = [ [0]*(lengthB + 1) for i in range(lengthA + 1) ]
    for i in range(lengthA + 1):
        for j in range(lengthB + 1):
            matrix[i][j] = 10000000
    matrix[0][0] = 0
    
    for i in range(1, lengthA + 1):
        for j in range(1, lengthB + 1):
            dist = compute_distance([seriesA[i-1], seriesB[j-1]]) ** 2
            minimum = min(matrix[i-1][j], matrix[i][j-1], matrix[i-1][j-1])
            matrix[i][j] = dist + minimum
    return matrix[-1][-1], matrix

def computeOptimalPath(matrix, seriesA, seriesB):
    assignment = []
    histogram_input = []
    n = len(matrix) - 1
    m = len(matrix[0]) - 1
    lastPoint = [seriesA[-1], seriesB[-1]]
    assignment.append(lastPoint)
    histogram_input.append(compute_distance(lastPoint) ** 2)
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
        histogram_input.append(compute_distance(point) ** 2)
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

# a = [(0.0, 0.0), (1.0, 0.0), (2.0, 1.0), (2.0, 2.0)]
# b = [(0.0, 0.0), (1.0, 0.0), (2.0, 1.0), (2.0, 2.0)]
# a = [(1, 0), (2, 0), (4, 2), (4, 3), (4, 3)]
# b = [(2, 2), (2, 2), (4, 2), (5, 2), (6, 4), (6, 5), (6, 5)]
# distance, matrix = dtw(a, b)
# print(matrix)
# print(distance)
# path = computeOptimalPath(matrix, a, b)
# path_distance = 0
# for j in range(len(path)):
#     path_distance += compute_distance_squared(path[j])
# print(path)
# print(path_distance)


### DTW DISTANCE HISTOGRAM ###

# inputs
traj1 = getPoints('./geolife-cars.csv', '128-20080503104400')
traj2 = getPoints('./geolife-cars.csv', '128-20080509135846')
# traj3 = getPoints('./geolife-cars.csv', '010-20081016113953')
# traj4 = getPoints('./geolife-cars.csv', '010-20080923124453')
# traj5 = getPoints('./geolife-cars.csv', '115-20080520225850')
# traj6 = getPoints('./geolife-cars.csv', '115-20080615225707')

# trajectory pair 1
# distance, matrix = frechetDistance(traj1, traj2)
# path, histogram_input = computeOptimalPath(matrix, traj1, traj2)

print("previous: ", 6.050266587370012)
distance, matrix = dtw(traj1, traj2)
print(distance)
path, histogram_input = computeOptimalPath(matrix, traj1, traj2)
print(sum(histogram_input))
path_distance = 0
for j in range(len(path)):
    path_distance += compute_distance(path[j]) ** 2
print(path_distance)

# trajectory pair 2
# distance, matrix = frechetDistance(traj3, traj4)
# path, histogram_input = computeOptimalPath(matrix, traj3, traj4)

# trajectory pair 3
# distance, matrix = frechetDistance(traj5, traj6)
# path, histogram_input = computeOptimalPath(matrix, traj5, traj6)
    
