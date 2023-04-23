import math, csv
import matplotlib.pyplot as plt
import matplotlib
from dtw import dtw, computeOptimalPath
from tsGreedy import ts_greedy

# to parse geolife file for desired trajectories
def get_points(file, trajectories):
    traj_dict = dict()
    for traj in trajectories:
        traj_dict[traj] = []
    with open(file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            num = row['id_']
            if num in traj_dict:
                traj_dict[num].append([float(row["x"]), float(row["y"])])
    return traj_dict

# to read trajectories from trajectory-ids.txt
def get_traj(file):
    with open(file) as f:
        trajectories = [line.strip() for line in f.readlines()]
    return trajectories

def simplify(pts_dict, e):
    mod_dict = dict()
    for key in pts_dict:
        mod_dict[key] = ts_greedy(pts_dict[key], e)
    return mod_dict

def center_approach_1(trajectories, pts_dict):
    center_traj = []
    m = 10000000
    for trajOne in trajectories:
        sum = 0
        for trajTwo in trajectories:
            if trajOne != trajTwo:
                distance, matrix = dtw(pts_dict[trajOne], pts_dict[trajTwo])
                sum += distance
        if sum < m:
            m = sum
            min_traj = trajOne
    avg_cost = m/len(trajectories)
    return min_traj, avg_cost

# Think of each trajectory Ti ∈ T as a function f(i) of time, and the goal is to compute a
# function that computes an average of these functions
def center_approach_2(trajectories, pts_dict):
    average_pts = dict()
    for traj in trajectories:
        for pt in pts_dict[traj]:
            # center trajectory will have a point at every 0.1-unit increment on the x-axis
            rounded = math.floor(pt[0]*10)/10
            if rounded not in average_pts:
                average_pts[rounded] = []
            average_pts[rounded].append(pt[1])
    center_traj = [0] * len(average_pts)
    index = 0
    for x_val in average_pts:
        y_val = sum(average_pts[x_val])/len(average_pts[x_val])
        center_traj[index] = [x_val, y_val]
        index += 1
    center_traj.sort(key=lambda x: -x[0])
    cost = 0
    for traj in trajectories:
        dist, matrix = dtw(center_traj, pts_dict[traj])
        cost += dist
    avg_cost = cost/len(trajectories)
    # print(avg_cost)
    return center_traj, avg_cost

# helper function to graph the trajectories, including the center trajectory
def plot_centering(trajectories, pts_dict, center1, center2):
    # plot trajectories
    for traj in trajectories:
        x = [pt[0] for pt in pts_dict[traj]]
        y = [pt[1] for pt in pts_dict[traj]]
        plt.plot(x, y, linewidth = 0.75, label=traj, color = 'black')

    # plot center1 trajectory
    x = [pt[0] for pt in center1]
    y = [pt[1] for pt in center1]
    plt.plot(x, y, linestyle = 'dashed', linewidth = 1.75, label='approach 1: center', color = '#30D5C8')
    
    # plot center2 trajectory
    x = [pt[0] for pt in center2]
    y = [pt[1] for pt in center2]
    plt.plot(x, y, linestyle = 'dashed', linewidth = 1.75, label='approach 2: center', color = 'green')

    # show legend and add to figure
    plt.legend(fontsize="8")
    plt.title("GeoLife Trajectory Centering - Approach 1 & 2")
    plt.xlabel("Longitude (in km)")
    plt.ylabel("Latitude (in km)")

    # show the figure
    plt.show()

if __name__ == "__main__": 
    # get trajectories from txt file
    trajectories = get_traj('trajectory-ids.txt')
    
    # get points from each trajectory, store in a dict where trajectory id is the key and 
    # array of points is the value
    pts_dict = get_points('geolife-cars-upd8.csv', trajectories)

    # approach 1
    # center_traj_1, avg_cost = center_approach_1(trajectories, pts_dict)
    # print(center_traj_1) # 115-20080707230001
    # print(avg_cost) # 27.85670694006133

    # approach 1 simplifications
    # simplified_pts_dict_03 = simplify(pts_dict, 0.03)
    # simplified_pts_dict_1 = simplify(pts_dict, 0.1)
    # simplified_pts_dict_3 = simplify(pts_dict, 0.3)
    # center_traj_1, avg_cost = center_approach_1(trajectories, simplified_pts_dict_3)
    # print(avg_cost)

    # plotting approach 1
    # plot_centering(trajectories, pts_dict, pts_dict[center_traj_1])
    
    # approach 2
    center_traj_2, cost = center_approach_2(trajectories, pts_dict)
    print(cost)
    
    # plotting approach 2
    plot_centering(trajectories, pts_dict, pts_dict['115-20080707230001'], center_traj_2)
    