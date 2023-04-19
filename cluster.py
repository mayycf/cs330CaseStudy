import math, csv, random
import matplotlib.pyplot as plt
import matplotlib
from dtw import dtw
from tsGreedy import ts_greedy
from center import center_approach_2

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

def random_lloyds(traj_dict, k, t_max):
    traj_list = [key for key in traj_dict]
    # clusters_dict = [] -> key = integer, value = set of traj ids
    clusters_dict = dict()
    # cluster_centers = [[]] -> array of array of points to store the center trajectory for each cluster
    cluster_centers = [0 for i in range(k)]
    num_per_cluster = int(len(traj_list)/k)
    for i in range(k):
        clusters_dict[i] = set()
        for j in range(num_per_cluster): # should each cluster be initialized to have the same number of trajectories?
            if len(traj_list) == 0:
                break
            selected = random.randint(0, len(traj_list) - 1)
            clusters_dict[i].add(traj_list[selected])
            traj_list.pop(selected)
    
    for num in clusters_dict:
        cluster_centers[num] = center_approach_2(clusters_dict[num], traj_dict)
        
    num_iter = 0
    changed = True
    while num_iter < t_max and changed:
        new_clusters_dict = recompute_center(traj_dict, cluster_centers, clusters_dict)
        num_iter += 1
        changed = False
        for num in range(len(cluster_centers)):
            new_center = center_approach_2(clusters_dict[num], traj_dict)
            if new_center != cluster_centers[num]:
                changed = True
            cluster_centers[num] = new_center
                
# returns: boolean (True if the old and new cluster dictionaries are the same, false otherwise)
def check_cluster_dicts(old, new):
    for key in old:
        if old[key] != new[key]:
            return False
    return True
            
def recompute_center(traj_dict, cluster_centers, clusters_dict):
    for i in range(len(cluster_centers)):
        clusters_dict[i] = set()
    for traj_key in traj_dict:
        cluster = -1
        min_dist = 10000000
        for num in range(len(cluster_centers)):
            dist, matrix = dtw(cluster_centers[num], traj_dict[traj_key])
            if dist <= min_dist:
                cluster = num
                min_dist = dist
        clusters_dict[cluster].add(traj_key)
    return clusters_dict

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
    simplified_pts_dict = simplify_pts(pts_dict, 0.03)
    print("created simplified_pts_dict")   
    random_lloyds(simplified_pts_dict, 10, 1)
    
