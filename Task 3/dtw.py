# NEED TO CHANGE, DIFFERENT FROM ASSIGNMENT 4

import math

# input: array of 2 tuples, [(x1, y1), (x2, y2)]
# output: returns the distance between them
def compute_distance_squared(pts):
    return ((pts[0][0] - pts[1][0])*(pts[0][0] - pts[1][0])) + ((pts[0][1] - pts[1][1])*(pts[0][1] - pts[1][1]))

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
            dist = compute_distance_squared([seriesA[i-1], seriesB[j-1]])
            minimum = min(matrix[i-1][j], matrix[i][j-1], matrix[i-1][j-1])
            matrix[i][j] = dist + minimum
    return matrix[-1][-1], matrix

def computeOptimalPath(matrix, seriesA, seriesB):
    assignment = []
    n = len(matrix) - 1
    m = len(matrix[0]) - 1
    while n > 0 or m > 0:
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
    assignment.reverse()
    return assignment

# a = [(0.0, 0.0), (1.0, 0.0), (2.0, 1.0), (2.0, 2.0)]
# b = [(0.0, 0.0), (1.0, 0.0), (2.0, 1.0), (2.0, 2.0)]
a = [(1, 0), (2, 0), (4, 2), (4, 3), (4, 3)]
b = [(2, 2), (2, 2), (4, 2), (5, 2), (6, 4), (6, 5), (6, 5)]
distance, matrix = dtw(a, b)
print(matrix)
print(distance)
path = computeOptimalPath(matrix, a, b)
path_distance = 0
for j in range(len(path)):
    path_distance += compute_distance_squared(path[j])
print(path)
print(path_distance)
    
