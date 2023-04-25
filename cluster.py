import math, csv, random
import matplotlib.pyplot as plt
import matplotlib
from dtw import dtw
from tsGreedy import ts_greedy
from center import center_approach_1

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
        # print(current_cost)
        num_iter += 1
        if previous_cost - current_cost < 10:
            changed = False
        previous_cost = current_cost
    center_plot_cluster = []
    for x in clusters_dict:
         center_plot_cluster.append(cluster_centers[x])
    print(cluster_centers)
    print(center_plot_cluster)
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
    
def plot_clustering(random_avg_cost, proposed_avg_cost):
    k = [4,6,8,10,12]
    costs = []
    # plot trajectories
    for i in range(len(k)):
        y = random_avg_cost[i][1]
        costs.append(y)
        
    plt.plot(k, costs, linewidth = 0.75, label = "random seeding", color='red', marker='o')
    
    costs = []
    # plot trajectories
    for i in range(len(k)):
        y = proposed_avg_cost[i][1]
        costs.append(y)
        
    plt.plot(k, costs, linewidth = 0.75, label = "proposed seeding", color='blue', marker='o')


    # show legend and add to figure
    plt.legend(fontsize="8")
    plt.title("GeoLife Average Clustering Costs - Random & Proposed")
    plt.xlabel("K values")
    plt.ylabel("Average Clustering Costs")
    
    plt.show()
    
def plot_iterations(avg_cost):
    iter = [1,2,3,4,5]
    costs = []
    # plot trajectories
    for i in range(len(iter)):
        y = avg_cost[i][1]
        costs.append(y)
        
    plt.plot(iter, costs, linewidth = 0.75, label = "cost", color='red', marker='o')
    plt.xticks(iter)

    # show legend and add to figure
    plt.legend(fontsize="8")
    plt.xlabel('Iteration')
    plt.ylabel('Average cost of clustering')
    plt.title('Comparison of seeding methods for k=8')
    plt.legend()
    plt.show()
    
    plt.show()
    
def plot_centers(trajectories, pts_dict):
    # plot trajectories
    count = 0
    colors = ['red', 'green', 'blue', 'black', 'pink', 'orange', 'brown', 'purple']
    
    for traj in trajectories:
        x = [pt[0] for pt in pts_dict[traj]]
        y = [pt[1] for pt in pts_dict[traj]]
        plt.plot(x, y, linewidth = 0.75, label=traj, color = colors[count])
        count += 1
        
    # show legend and add to figure
    plt.legend(fontsize="8")
    plt.title("Center Trajectories with Proposed Seeding and k = 8")
    plt.xlabel("Longitude (in km)")
    plt.ylabel("Latitude (in km)")

    # show the figure
    plt.show()
    
if __name__ == "__main__": 
    # dictionary with trajectory id as the key and arrays of pts as the value
    pts_dict = get_points('geolife-cars-upd8.csv')
    # simplified_pts_dict = simplify_pts(pts_dict, 0.2)
    
    # proposed seeding, k = 8, epsilon = 0.2
    cluster_centers = ['115-20080639682095', '128-20080517020041', '010-20081012234529', '128-20080704130347', '153-20080712125122', '163-20080704145434', '115-20080611231533', '115-20080508230928']
    
    ### RANDOM SEEDING ###
    # print("cost with k = 4 & random seeding: ", lloyds_algorithm(simplified_pts_dict, 4, 5, "random"))
    # print("cost with k = 6 & random seeding: ", lloyds_algorithm(simplified_pts_dict, 6, 5, "random"))
    # print("cost with k = 8 & random seeding: ", lloyds_algorithm(simplified_pts_dict, 8, 5, "random"))
    # print("cost with k = 10 & random seeding: ", lloyds_algorithm(simplified_pts_dict, 10, 5, "random"))
    # print("cost with k = 12 & random seeding: ", lloyds_algorithm(simplified_pts_dict, 12, 5, "random"))

    ### PROPOSED SEEDING ###
    # print("cost with k = 4 & proposed seeding: ", lloyds_algorithm(simplified_pts_dict, 4, 5, "proposed"))
    # print("cost with k = 6 & proposed seeding: ", lloyds_algorithm(simplified_pts_dict, 6, 5, "proposed"))
    # print("cost with k = 8 & proposed seeding: ", lloyds_algorithm(simplified_pts_dict, 8, 5, "proposed"))
    # print("cost with k = 10 & proposed seeding: ", lloyds_algorithm(simplified_pts_dict, 10, 5, "proposed"))
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
    
    # let random_cost_it and proposed_cost_it be the matrices of the cost of clustering such that 
    # matrix[i][j] represents the cost of clustering in the ith run of Lloyd’s algorithm for jth iteration
    
    random_cost_it = [  [132424.86063889405, 132424.25214825838, 132409.66065464745],
                        [15455.728291958487, 15524.011679553181, 14927.859591719749],
                        [14851.559098017407, 15377.954001121601, 14792.085315196475],
                        [14838.436015882378, 15370.178408613201, 14792.085315196475],
                        [14833.551955813587, 15370.178408613201, 14792.085315196475]]
    
    random_average_cost_it = [[1, 132419.591147], [2, 15302.5331877], [3, 15007.1994714],
                              [4, 15000.2332466], [5, 14998.6052265]]
    
    proposed_cost_it = [    [2104.59344517931, 2184.707194847631, 2112.557579884904],
                            [1481.9830313828543, 1481.9830313828543, 1481.9830313828543],
                            [1481.9830313828543, 1481.9830313828543, 1481.9830313828543],
                            [1481.9830313828543, 1481.9830313828543, 1481.9830313828543],
                            [1481.9830313828543, 1481.9830313828543, 1481.9830313828543]]

    proposed_average_cost_it = [[1, 2133.95273997], [2, 1481.98303138], [3, 1481.98303138],
                              [4, 1481.98303138], [5, 1481.98303138]]

    # plot_clustering(random_clustering_avg_costs, proposed_clustering_avg_costs)
    # plot_iterations(random_average_cost_it)
    # plot_iterations(proposed_average_cost_it)
    plot_centers(cluster_centers, pts_dict)