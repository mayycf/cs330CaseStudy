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
 
    def count_neighbors(self, x, y, radius):
        return self._count_neighbors(self.root, x, y, radius)
 
    def _count_neighbors(self, node, x, y, radius):
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
            count += self._count_neighbors(node.left, x, y, radius)
        if x + radius >= point[axis]:
            count += self._count_neighbors(node.right, x, y, radius)
 
        return count
    
points = [(2,3), (5,4), (9,6), (4,7), (8,1), (7,2)]
tree = KDTree(points)
count = tree.count_neighbors(1, 1, 1)
print(count)