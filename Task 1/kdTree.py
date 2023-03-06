import csv

def compute_distance(pts):
    return math.sqrt(((pts[0][0] - pts[1][0])*(pts[0][0] - pts[1][0])) + ((pts[0][1] - pts[1][1])*(pts[0][1] - pts[1][1])))

class Node:
    def __init__(self, point, depth):
        self.point = point
        self.left = None
        self.right = None
        self.depth = depth
 
class KDTree:
    def __init__(self, points):
        self.root = self.build(points, 0)
 
    def build(self, points, depth):
        n = len(points)
        if n <= 0:
            return None
        axis = depth % len(points[0])
        sorted_points = sorted(points, key=lambda point: point[axis])
        mid = n // 2
        node = Node(sorted_points[mid], depth)
        node.left = self.build(sorted_points[:mid], depth+1)
        node.right = self.build(sorted_points[mid+1:], depth+1)
        return node
 
    def density(self, x, y, radius):
        return self._density(self.root, x, y, radius)
 
    def _density(self, node, x, y, radius):
        if node is None:
            return 0
 
        point = node.point
        dx = x - point[0]
        dy = y - point[1]
        if dx**2 + dy**2 <= radius**2:
            count = 1
        else:
            count = 0
 
        axis = node.depth % len(point)
        if x - radius <= point[axis]:
            count += self._density(node.left, x, y, radius)
        if x + radius >= point[axis]:
            count += self._density(node.right, x, y, radius)
 
        return count

### method to parse through csv file ###
def getPoints(x):
    points = []
    with open('./geolife-cars-ten-percent.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        if x == "all":
            for row in reader:
                points.append([float(row["x"]), float(row["y"])])
        else:
            for row in reader:
                if (row['id_'] == x):
                    points.append([float(row["x"]), float(row["y"])])
    return points

### TESTING ###
pts = getPoints("all")
tree = KDTree(pts)
count = tree.density(1, 1, 5)
print(count)
hubs = hubs(pts, tree, 3, 10)
print(hubs)


