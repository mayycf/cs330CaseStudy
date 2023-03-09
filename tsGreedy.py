import matplotlib.pyplot as plt
import matplotlib
import csv
from epsilon import d

# TS-Greedy function that finds a "pivot" that is the maximum point that is outside the error bounds
# and recurses through the left and right side of the pivot to find more "pivot"
# points to add to the final trajectory. 
def ts_greedy(T,e):
    n = len(T)
    if len(T) == 1:
        return T
    segment = (T[0],T[-1])
    final = [T[0]]
    maximum = e
    index = 0
    for point in range(n):
        errdist = d(T[point], segment)
        if errdist > maximum:
            maximum = errdist 
            index = point
            
    if maximum != e:
        left = ts_greedy(T[0:index+1], e)
        right = ts_greedy(T[index:], e)
        final.extend(left[1:-1][0:])
        final.extend(right[:-1])        
    final.append(T[-1])
    return final

# helper function that parces the GeoLife file to find the trajectory of interest
def getPoints(x):
    points = []
    with open("geolife-cars.csv", newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if(row['id_'] == x):
                points.append([float(row["x"]), float(row["y"])])
    return points

# helper function to graph the trajectories
def plotit(T, e):
    # change font size
    matplotlib.rcParams.update({'font.size': 7})

    # create figure
    figure = plt.figure(figsize=(7, 4), dpi=120)

    # space for unsimplified curve
    splot = plt.subplot()
    x = [i[0] for i in T]
    y = [i[1] for i in T]
    splot.plot(x, y, linewidth = 2, label='n={}, no simplification'.format(len(T)))

    # code for the simplified curve 
    simplified = ts_greedy(T, e)
    x = [i[0] for i in simplified]
    y = [i[1] for i in simplified]
    splot.plot(x, y, marker = "o", markersize = 3.5, linestyle='dashed', linewidth = 1.5, label='n={}, ε={}'.format(len(simplified), e))
    
    # Print the points to calculate compression ratio
    print("This is the length of the original list of points: ", len(T))
    print("This is the length of the simplified trajectory: ", len(simplified))
    print("This is the compression ratio: ", len(T)/len(simplified))

    # show legend and add to figure
    splot.legend()
    splot.set_title("GeoLife Trajectory Simplification")
    plt.xlabel("Longitude (in km)")
    plt.ylabel("Latitude (in km)")
    figure.add_subplot(splot)

    # show the figure
    plt.show()

if __name__ == "__main__" :
    T = getPoints("128-20080503104400")
    e = 0.3
    # T = getPoints("010-20081016113953")
    # e = 0.03
    # T = getPoints("115-20080520225850")
    # e = 0.03
    # T = getPoints("115-20080615225707")
    # e = 0.03

    plotit(T, e) 
    # print("These are the simplification results:", ts_greedy(T,e))
    
    # TESTS:
    # "128-20080503104400" e = 0, 319 points
    # "128-20080503104400" e = .03, 18 points 
    # "128-20080503104400" e = .1, 14 points 
    # "128-20080503104400" e = .3, 5 points