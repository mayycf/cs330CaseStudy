import math, csv, random
import matplotlib.pyplot as plt
import matplotlib
from dtw import dtw
from tsGreedy import ts_greedy
from center import center_approach_1, center_approach_2

# to parse geolife file for ALL trajectories
# returns: dictionary with trajectory id as the key and arrays of pts as the value
def get_points(file):
    traj_dict = dict()
    with open(file, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            num = row['id_']
            if num not in traj_dict:
                traj_dict[num] = []
            traj_dict[num].append([float(row["x"]), float(row["y"])])
    return traj_dict

def random_seeding(traj_dict, k):
    traj_list = [key for key in traj_dict]
    # clusters_dict = [] -> key = integer, value = set of traj ids
    clusters_dict = dict()
    num_per_cluster = int(len(traj_list)/k)
    for i in range(k):
        clusters_dict[i] = []
        for j in range(num_per_cluster):
            if len(traj_list) == 0:
                break
            selected = random.randint(0, len(traj_list) - 1)
            clusters_dict[i].append(traj_list[selected])
            traj_list.pop(selected)
    return clusters_dict

# input: traj_dict -> key = traj id, value = array of points in that trajectory
def proposed_seeding(traj_dict, k):
    # traj_list - list of trajectories by traj id (i.e. "115-20080527225031")
    traj_list = [key for key in traj_dict]
    # clusters_dict = dict() -> key = integer (0, ..., k-1), value = set of traj ids in that cluster
    clusters_dict = dict()
    # as you find centers using k-means++, append them to the cluster_centers array
    cluster_centers = []
    
    ### YOUR CODE HERE ###
    # use k-means++ to find the ideal centers for the clusters to begin with
    # as you find each center, append the traj_id to cluster_centers[]
    # after finding the k cluster centers, call reassignment to populate clusters_dict with 
    # the trajectories that should be in each cluster    
    
    reassignment(traj_dict, cluster_centers, clusters_dict)
    return clusters_dict

def lloyds_algorithm(traj_dict, k, t_max, seed_method):
    if seed_method == "random":
        clusters_dict = random_seeding(traj_dict, k)
    elif seed_method == "proposed":
        clusters_dict = proposed_seeding(traj_dict, k)
    # cluster_centers = [] -> array of traj ids to store the center trajectory for each cluster
    cluster_centers = [None for i in range(k)]
        
    previous_cost = 10000000
    # print(previous_cost)
    num_iter = 0
    changed = True
    while num_iter < t_max and changed:
        # compute the center for each cluster
        for key in clusters_dict:
            traj_id, cost = center_approach_1(clusters_dict[key], traj_dict)
            cluster_centers[key] = traj_id 
        # assign each trajectory to the cluster whose center trajectory is closest
        # find the current_cost of that clustering
        current_cost = reassignment(traj_dict, cluster_centers, clusters_dict)
        # print(current_cost)
        num_iter += 1
        if previous_cost - current_cost < 10:
            changed = False
        previous_cost = current_cost
        print(current_cost)   
    return current_cost
       
def reassignment(traj_dict, cluster_centers, clusters_dict):
    cost = 0
    for cluster_key in clusters_dict:
        clusters_dict[cluster_key] = []
    for traj_key in traj_dict:
        cluster = -1
        min_dist = 10000000
        for num in range(len(cluster_centers)):
            dist, matrix = dtw(traj_dict[cluster_centers[num]], traj_dict[traj_key])
            if dist <= min_dist:
                cluster = num
                min_dist = dist
        clusters_dict[cluster].append(traj_key)
        cost += min_dist
    return cost

# returns: dictionary of trajectories with simplified points
def simplify_pts(pts_dict, e):
    simplified_pts_dict = dict()
    for key in pts_dict:
        sim_traj = ts_greedy(pts_dict[key], e)
        simplified_pts_dict[key] = sim_traj
    return simplified_pts_dict
    
if __name__ == "__main__": 
    # dictionary with trajectory id as the key and arrays of pts as the value
    pts_dict = get_points('geolife-cars-upd8.csv')
    simplified_pts_dict = simplify_pts(pts_dict, 0.2)
    
    # Evaluate the cost of clustering for k = 4,6,8,10,12 for the random and the proposed seeding methods
    # Evaluate the cost three times for each value of k, and report the average
    
    print("cost with k = 4 & random seeding: ", lloyds_algorithm(simplified_pts_dict, 4, 5, "random"))
    print("cost with k = 4 & random seeding: ", lloyds_algorithm(simplified_pts_dict, 4, 5, "random"))
    print("cost with k = 4 & random seeding: ", lloyds_algorithm(simplified_pts_dict, 4, 5, "random"))
    print("cost with k = 6 & random seeding: ", lloyds_algorithm(simplified_pts_dict, 6, 5, "random"))
    print("cost with k = 6 & random seeding: ", lloyds_algorithm(simplified_pts_dict, 6, 5, "random"))
    print("cost with k = 6 & random seeding: ", lloyds_algorithm(simplified_pts_dict, 6, 5, "random"))
    print("cost with k = 8 & random seeding: ", lloyds_algorithm(simplified_pts_dict, 8, 5, "random"))
    print("cost with k = 8 & random seeding: ", lloyds_algorithm(simplified_pts_dict, 8, 5, "random"))
    print("cost with k = 8 & random seeding: ", lloyds_algorithm(simplified_pts_dict, 8, 5, "random"))
    print("cost with k = 10 & random seeding: ", lloyds_algorithm(simplified_pts_dict, 10, 5, "random"))
    print("cost with k = 10 & random seeding: ", lloyds_algorithm(simplified_pts_dict, 10, 5, "random"))
    print("cost with k = 10 & random seeding: ", lloyds_algorithm(simplified_pts_dict, 10, 5, "random"))
    print("cost with k = 12 & random seeding: ", lloyds_algorithm(simplified_pts_dict, 12, 5, "random"))
    print("cost with k = 12 & random seeding: ", lloyds_algorithm(simplified_pts_dict, 12, 5, "random"))
    print("cost with k = 12 & random seeding: ", lloyds_algorithm(simplified_pts_dict, 12, 5, "random"))