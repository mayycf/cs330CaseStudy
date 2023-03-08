import matplotlib.pyplot as plt
import matplotlib
import csv
from epsilon import d

def ts_greedy(T,e):
    # print(plt)
    # for each iteration, check the largest point where the error is > e
    # that is the first line, then we move the end to the point we just found, 
    # and we do it again.
    # print("We start with: ", T)
    n = len(T)
    if len(T) == 1:
        return T
    segment = (T[0],T[-1])
    final = [T[0]]
    maximum = e
    # bp = 0
    index = 0
    for point in range(n):
        errdist = d(T[point], segment)
        if errdist > maximum:
            maximum = errdist #x is the new point tuple
            # bp = T[point]
            # print("yea this happened")
            index = point
            
    # print("BP: ", bp)
    if maximum != e:
        # print("Recurse!")
        left = ts_greedy(T[0:index+1], e)
        right = ts_greedy(T[index:], e)
        # print("If final: ", final)
        # print("Left: ", left)
        # print("Right: ", right)
        final.extend(left[1:-1][0:])
        final.extend(right[:-1])        
    final.append(T[-1])
    # print("Final :", final)
    return final

def getPoints(x):
    points = []
    with open("geolife-cars.csv", newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if(row['id_'] == x):
                points.append([float(row["x"]), float(row["y"])])
    return points

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

    simplified = ts_greedy(T, e)
    x = [i[0] for i in simplified]
    y = [i[1] for i in simplified]
    splot.plot(x, y, marker = "o", markersize = 3.5, linestyle='dashed', linewidth = 1.5, label='n={}, ε={}'.format(len(T), e))
    
     
    print("This is the length of the original list of points: ", len(T))
    print("This is the length of the simplified trajectory: ", len(simplified))

    # show legend and add to figure
    splot.legend()
    splot.set_title("GeoLife Trajectory Simplification")
    figure.add_subplot(splot)

    # show the figure
    plt.show()

if __name__ == "__main__" :
    # T = getPoints("128-20080503104400")
    # e = 0.3
    # T = getPoints("010-20081016113953")
    # e = 0.03
    # T = getPoints("115-20080520225850")
    # e = 0.03
    T = getPoints("115-20080615225707")
    e = 0.03
    

    plotit(T, e)
    
    # print(ts_greedy(T,e))
    
    # TESTS:
    # "128-20080503104400" e = 0, 319 points
    # "128-20080503104400" e = .03, 18 points 
    # "128-20080503104400" e = .1, 14 points 
    # "128-20080503104400" e = .3, 5 points