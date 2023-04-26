import math, csv, random
import matplotlib.pyplot as plt
import matplotlib
from dtw import dtw, computeOptimalPath
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
        if previous_cost - current_cost < 2:
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
            assignment, histogram_input = computeOptimalPath(matrix, traj_dict[cluster_centers[num]], traj_dict[traj_key])
            distance = math.sqrt(dist/len(assignment))
            if distance <= min_dist:
                cluster = num
                min_dist = distance
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
    plt.title('Average Cost of Clustering Over Iterations with k=8 - Proposed Seeding')
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
    simplified_pts_dict = simplify_pts(pts_dict, 0.2)
    
    # proposed seeding, k = 8, epsilon = 0.2
    cluster_centers = ['153-20080929141601', '115-20080611231533', '128-20080704130347', '128-20080517020041', '010-20081005235128', '163-20080428134620', '115-20080639197975', '115-20080508230928']

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
    
    random_clustering_costs = {4: [1385.8662908176066, 1374.4261225016078, 1367.2171332892922],
                         6: [1368.5669290445742, 1361.6228691128626, 1362.1765400571962],
                         8: [1358.9005768503694, 1359.01993380758, 1346.311433033083],
                         10: [1344.091815944868, 1342.0209605943817, 1338.1736834488881],
                         12: [1335.3650102681445, 1342.4478466953378, 1342.8198562545997]}
    
    random_clustering_avg_costs = [[4, 1375.836515536169], [6, 1364.122112738211], 
                                   [8, 1354.743981230344], [10, 1341.4288199960458], 
                                   [12, 1340.2109044060273]]
    
    proposed_clustering_costs = {4 :[604.9894406726208, 604.9894406726208, 604.9894406726208], 
                                 6: [376.5999558706342, 376.5999558706342, 376.5999558706342], 
                                 8: [286.8021826780779, 286.8021826780779, 286.8021826780779], 
                                 10: [283.6776173914242, 283.6776173914242, 283.6776173914242], 
                                 12: [236.77198753337703, 236.77198753337703, 236.77198753337703]}
    
    proposed_clustering_avg_costs = [[4, 604.9894406726208], [6, 376.5999558706342], 
                                     [8, 286.8021826780779], [10, 283.6776173914242], 
                                     [12, 236.77198753337703]]
    
    # let random_cost_it and proposed_cost_it be the matrices of the cost of clustering such that 
    # matrix[i][j] represents the cost of clustering in the ith run of Lloyd’s algorithm for jth iteration
    
    random_cost_it = [  [1512.9484669348708, 1514.5984505297158, 1514.0825896081628],
                        [1352.5928716366775, 1362.4144914408762, 1361.5022615484215],
                        [1346.523431750786, 1359.1864389044963, 1359.106722065497],
                        [1346.311433033083, 1358.9005768503694, 1359.01993380758],
                        [1346.311433033083, 1358.9005768503694, 1359.01993380758]]
    
    random_average_cost_it = [[1, 1513.8765023575834], [2, 1358.836541541992], 
                              [3, 1354.9388642402598], [4, 1354.743981230344], 
                              [5, 1354.743981230344]]
    
    proposed_cost_it = [    [321.23064779367456, 332.9036323812487, 341.36424834986354],
                            [286.8021826780779, 286.8021826780779, 286.8021826780779],
                            [286.8021826780779, 286.8021826780779, 286.8021826780779],
                            [286.8021826780779, 286.8021826780779, 286.8021826780779],
                            [286.8021826780779, 286.8021826780779, 286.8021826780779]]

    proposed_average_cost_it = [[1, 331.83284284159566], [2, 286.8021826780779], 
                                [3, 286.8021826780779], [4, 286.8021826780779], 
                                [5, 286.8021826780779]]

    plot_clustering(random_clustering_avg_costs, proposed_clustering_avg_costs)
    # plot_iterations(random_average_cost_it)
    # plot_iterations(proposed_average_cost_it)
    # plot_centers(cluster_centers, pts_dict)