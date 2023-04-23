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
    # traj_centroid_dist - key = traj id (i.e. "115-20080527225031"), value = distance from nearest centroid
    traj_centroid_dist = dict()
    # clusters_dict = dict() -> key = integer (0, ..., k-1), value = array of traj ids in that cluster
    clusters_dict = dict()
    for i in range(k):
        clusters_dict[i] = []
    # keep track of traj ids that will serve as the cluster centers
    cluster_centers = []
    
    # first center, randomly selected
    c1 = random.randint(0, len(traj_list) - 1)
    cluster_centers.append(traj_list[c1])
    for traj_key in traj_dict:
        dist, matrix = dtw(traj_dict[cluster_centers[0]], traj_dict[traj_key])
        traj_centroid_dist[traj_key] = dist

    # select all other centers
    for i in range(k-1):
        new_centroid = max(traj_centroid_dist, key = traj_centroid_dist.get)
        cluster_centers.append(new_centroid)
        for traj_key in traj_centroid_dist:
            dist, matrix = dtw(traj_dict[cluster_centers[-1]], traj_dict[traj_key])
            if dist < traj_centroid_dist[traj_key]:
                traj_centroid_dist[traj_key] = dist

    # reassignment populates clusters_dict with the trajectories that should be in each cluster    
    previous_cost = reassignment(traj_dict, cluster_centers, clusters_dict)
    return clusters_dict, previous_cost

def lloyds_algorithm(traj_dict, k, t_max, seed_method): 
    if seed_method == "random":
        clusters_dict = random_seeding(traj_dict, k)
        previous_cost = 10000000
    elif seed_method == "proposed":
        clusters_dict, previous_cost = proposed_seeding(traj_dict, k)
        print(previous_cost)
    # cluster_centers = [] -> array of traj ids to store the center trajectory for each cluster
    cluster_centers = [None for i in range(k)]
        
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
        print(current_cost)
        num_iter += 1
        if previous_cost - current_cost < 10:  
            changed = False
        previous_cost = current_cost   
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
    # pts_dict = get_points('geolife-cars-upd8.csv')
    # simplified_pts_dict = simplify_pts(pts_dict, 0.2)
    
    # Evaluate the cost of clustering for k = 4,6,8,10,12 for the random and the proposed seeding methods
    # Evaluate the cost three times for each value of k, and report the average
    
    # print("cost with k = 4 & proposed seeding: ", lloyds_algorithm(simplified_pts_dict, 4, 5, "proposed"))
    # print("cost with k = 4 & proposed seeding: ", lloyds_algorithm(simplified_pts_dict, 4, 5, "proposed"))
    # print("cost with k = 4 & proposed seeding: ", lloyds_algorithm(simplified_pts_dict, 4, 5, "proposed"))
    # print("cost with k = 6 & proposed seeding: ", lloyds_algorithm(simplified_pts_dict, 6, 5, "proposed"))
    # print("cost with k = 6 & proposed seeding: ", lloyds_algorithm(simplified_pts_dict, 6, 5, "proposed"))
    # print("cost with k = 6 & proposed seeding: ", lloyds_algorithm(simplified_pts_dict, 6, 5, "proposed"))
    # print("cost with k = 8 & proposed seeding: ", lloyds_algorithm(simplified_pts_dict, 8, 5, "proposed"))
    # print("cost with k = 8 & proposed seeding: ", lloyds_algorithm(simplified_pts_dict, 8, 5, "proposed"))
    # print("cost with k = 8 & proposed seeding: ", lloyds_algorithm(simplified_pts_dict, 8, 5, "proposed"))
    # print("cost with k = 10 & proposed seeding: ", lloyds_algorithm(simplified_pts_dict, 10, 5, "proposed"))
    # print("cost with k = 10 & proposed seeding: ", lloyds_algorithm(simplified_pts_dict, 10, 5, "proposed"))
    # print("cost with k = 10 & proposed seeding: ", lloyds_algorithm(simplified_pts_dict, 10, 5, "proposed"))
    # print("cost with k = 12 & proposed seeding: ", lloyds_algorithm(simplified_pts_dict, 12, 5, "proposed"))
    # print("cost with k = 12 & proposed seeding: ", lloyds_algorithm(simplified_pts_dict, 12, 5, "proposed"))
    # print("cost with k = 12 & proposed seeding: ", lloyds_algorithm(simplified_pts_dict, 12, 5, "proposed"))
    
    random_clustering_costs = {4: [38438.828109556445, 38438.828109556445, 32845.965655742526],
                         6: [26574.452578489625, 15481.756895123717, 15488.320420582688],
                         8: [14833.551955813587, 15370.178408613201, 14792.085315196475],
                         10: [14787.456677584803, 14696.415594061898, 14788.535401773328],
                         12: [14780.98240174656, 14739.241300043663, 14669.49297809701]}
    
    random_clustering_avg_costs = [[4, 36574.540624951806], [6, 19181.509964732013], 
                                   [8, 14998.605226541089], [10, 14757.469224473343], 
                                   [12, 14729.905559962412]]
    
    proposed_clustering_costs = {4 :[23443.528627308213, 23443.528627308213, 23443.528627308213], 
                                 6: [8665.320820637857, 8665.320820637857, 8665.320820637857], 
                                 8: [1481.9830313828543, 1481.9830313828543, 1481.9830313828543], 
                                 10: [1063.145425272224, 1434.608495500635, 1062.966680372892], 
                                 12: [1030.73445944251, 1030.73445944251, 1030.73445944251]}
    
    proposed_clustering_avg_costs = [[4, 23443.528627308213], [6, 8665.320820637857], 
                                     [8, 1481.9830313828543], [10, 1186.9068670485835], 
                                     [12, 1030.73445944251]]

    
    