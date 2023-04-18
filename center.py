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

def center_approach_1(trajectories, pts_dict):
    # CODE FROM TASK 1, NEED FOR DTW
    # I think all you need is distance
    # distance, matrix = dtw(trajOne, trajTwo)
    pass

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
    return sorted(center_traj, key=lambda x: x[0])

# helper function to graph the trajectories, including the center trajectory
def plot_centering(trajectories, pts_dict, center):
    # plot trajectories
    for traj in trajectories:
        x = [pt[0] for pt in pts_dict[traj]]
        y = [pt[1] for pt in pts_dict[traj]]
        plt.plot(x, y, linewidth = 0.75, label=traj, color = 'black')

    # plot center trajectory
    x = [pt[0] for pt in center]
    y = [pt[1] for pt in center]
    plt.plot(x, y, linestyle = 'dashed', linewidth = 2, label='center', color = 'blue')

    # show legend and add to figure
    plt.legend(fontsize="8")
    plt.title("GeoLife Trajectory Centering")
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
    
    # approach 2
    # center_traj_2 = center_approach_2(trajectories, pts_dict)
    
    # plotting approach 2
    # plot_centering(trajectories, pts_dict, center_traj_2)
    