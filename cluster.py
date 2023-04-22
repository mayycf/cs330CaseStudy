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
    # clusters_dict = dict() -> key = integer (0, ..., k-1), value = array of traj ids in that cluster
    clusters_dict = dict()
    for i in range(k):
        clusters_dict[i] = []
    # keep track of traj ids that will serve as the cluster centers
    cluster_centers = []
    
    # first center, randomly selected
    c1 = random.randint(0, len(traj_list) - 1)
    cluster_centers.append(traj_list[c1])

    # select all other centers
    for i in range(k-1):
        max_d = 0     # maximum distance from a point to a centroid
        max_traj = 0    # max traj key, max associated cluster
        for num in range(len(cluster_centers)):
            for traj_key in traj_list:
                dist, matrix = dtw(traj_dict[cluster_centers[num]], traj_dict[traj_key])
                if dist > max_d:
                    max_d = dist
                    max_traj = traj_key

        cluster_centers.append(max_traj)

    print("clusters: ", cluster_centers)

    # reassignment populates clusters_dict with the trajectories that should be in each cluster    
    reassignment(traj_dict, cluster_centers, clusters_dict)
    return clusters_dict

def proposed_seeding2(traj_dict, k):
    # traj_list - list of trajectories by traj id (i.e. "115-20080527225031")
    traj_list = [key for key in traj_dict]
    # clusters_dict = dict() -> key = integer (0, ..., k-1), value = set of traj ids in that cluster
    clusters_dict = dict()
    # as you find centers using k-means++, append them to the cluster_centers array
    cluster_centers = []
    
    # first center
    c1 = random.randint(0, len(traj_list) - 1)
    cluster_centers.append(traj_list[c1])
    clusters_dict[traj_list[c1]] = []
    # select all other centers
    # for each data point, we need to calculate its closest centroid. 
    # Then for each of these distances, choose the largest one as the next centroid until we reach k centroids.
    for i in range(k-1):
          # maximum distance from a point to a centroid
        max_traj = 0    # max traj key, max associated cluster
        next_center = 0
        # for each cluster center? 
        for cluster_key in clusters_dict:
            clusters_dict[cluster_key] = []
            
        # reassign each trajectory to a cluster
        for traj_key in traj_dict:
            cluster = -1
            min_dist = 10000000
            for num in range(len(cluster_centers)):
                dist, matrix = dtw(traj_dict[cluster_centers[num]], traj_dict[traj_key])
                if dist <= min_dist:
                    cluster = cluster_centers[num]
                    min_dist = dist
            if min_dist >= max_traj:
                max_traj = min_dist
                next_center = traj_key
            # print("cluster!!!!", cluster)
            clusters_dict[cluster].append(traj_key)
        
        cluster_centers.append(next_center)
        clusters_dict[next_center] = []   

    print("clusters: ", cluster_centers)
    # as you find each center, append the traj_id to cluster_centers[]
    # after finding the k cluster centers, call reassignment to populate clusters_dict with 
    # the trajectories that should be in each cluster    
    for cluster_key in clusters_dict:
            clusters_dict[cluster_key] = []
            
    for traj_key in traj_dict:
            cluster = -1
            min_dist = 10000000
            for num in range(len(cluster_centers)):
                dist, matrix = dtw(traj_dict[cluster_centers[num]], traj_dict[traj_key])
                if dist <= min_dist:
                    cluster = cluster_centers[num]
                    min_dist = dist
            if min_dist >= max_traj:
                max_traj = min_dist
                next_center = traj_key
            clusters_dict[cluster].append(traj_key)
    # min_cost = reassignment(traj_dict, cluster_centers, clusters_dict)
    return clusters_dict

def lloyds_algorithm(traj_dict, k, t_max, seed_method): 
    if seed_method == "random":
        clusters_dict = random_seeding(traj_dict, k)
    elif seed_method == "proposed":
        clusters_dict = proposed_seeding(traj_dict, k)
    # cluster_centers = [] -> array of traj ids to store the center trajectory for each cluster
    cluster_centers = [None for i in range(k)]
        
    previous_cost = 10000000
    print(previous_cost)
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

# helper function to plot the average cost of clustering vs. k
def plot_avg_cost_k(random_cluster, proposed_cluster):
    # plot random cluster
    x = [pt[0] for pt in random_cluster]
    y = [pt[1] for pt in random_cluster]
    plt.plot(x, y, marker="o", linewidth = 1, label='Random Seeding', color = 'blue')

    # plot proposed cluster
    # x = [pt[0] for pt in proposed_cluster]
    # y = [pt[1] for pt in proposed_cluster]
    # plt.plot(x, y, linewidth = 1, label='Proposed Seeding', color = 'green')

    # show legend and add to figure
    plt.legend(fontsize="8")
    plt.title("Average Cost of Clustering vs. K")
    plt.xlabel("K")
    plt.ylabel("Average Cost")

    # show the figure
    plt.show()
    
if __name__ == "__main__": 
    # dictionary with trajectory id as the key and arrays of pts as the value
    pts_dict = get_points('geolife-cars-upd8.csv')
    simplified_pts_dict = simplify_pts(pts_dict, 0.8)
    
    # Evaluate the cost of clustering for k = 4,6,8,10,12 for the random and the proposed seeding methods
    # Evaluate the cost three times for each value of k, and report the average
    
    # print("cost with k = 4 & random seeding")
    # print(lloyds_algorithm(simplified_pts_dict, 4, 5, "random"))
    # print("cost with k = 6 & random seeding")
    # print(lloyds_algorithm(simplified_pts_dict, 6, 5, "random"))
    # print("cost with k = 8 & random seeding")
    # print(lloyds_algorithm(simplified_pts_dict, 8, 5, "random"))
    # print("cost with k = 10 & random seeding")
    # print(lloyds_algorithm(simplified_pts_dict, 10, 5, "random"))
    # print("cost with k = 12 & random seeding")
    # print(lloyds_algorithm(simplified_pts_dict, 12, 5, "random"))
    
    # Plotting
    random_clustering_costs = {4: [38438.828109556445, 38438.828109556445, 32845.965655742526],
                         6: [26574.452578489625, 15481.756895123717, 15488.320420582688],
                         8: [14833.551955813587, 15370.178408613201, 14792.085315196475],
                         10: [14787.456677584803, 14696.415594061898, 14788.535401773328],
                         12: [14780.98240174656, 14739.241300043663, 14669.49297809701]}
    
    random_clustering_avg_costs = [[4, 36574.540624951806], [6, 19181.509964732013], 
                                   [8, 14998.605226541089], [10, 14757.469224473343], 
                                   [12, 14729.905559962412]]
    
    proposed_clustering_costs = {}
    
    proposed_clustering_avg_costs = []
    
    # plot_avg_cost_k(random_clustering_avg_costs, proposed_clustering_avg_costs)