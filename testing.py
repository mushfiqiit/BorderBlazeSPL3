import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import Delaunay
from collections import defaultdict
import open3d as o3d

destination_path = "build4.pts"
# Generate random 2D points
point_cloud_data = np.loadtxt(destination_path, skiprows=1, max_rows=10000)
n = len(point_cloud_data)
point_cloud_data[:, 2] = 0
point_cloud_data = point_cloud_data[:, :3]
points_2d = []

for i in range(n):
    points_2d.append([point_cloud_data[i][0], point_cloud_data[i][1]])

points_2d = np.array(points_2d)  # Convert to NumPy array

# Apply Delaunay triangulation
tri = Delaunay(points_2d)

# Create a dictionary to store the count for each edge
edge_triangle_count = defaultdict(int)

# Iterate over each simplex to collect unique edges
for simplex in tri.simplices:
    for i in range(3):  # A triangle has three edges
        edge = tuple(sorted([simplex[i], simplex[(i + 1) % 3]]))
        edge_triangle_count[edge] += 1

# Convert the set of edges to a list for easier handling
edges_list = list(edge_triangle_count.keys())

isBoundary = [0] * n

# Identify boundary points
for edge in edges_list:
    point1, point2 = edge
    if edge_triangle_count[edge] <= 1:
        isBoundary[point1] = 1
        isBoundary[point2] = 1

red_points = []
green_points = []

for i in range(n):
    if isBoundary[i] == 1:
        red_points.append(point_cloud_data[i])
    else:
        green_points.append(point_cloud_data[i])

# Create Open3D point cloud objects
red_point_cloud = o3d.geometry.PointCloud()
red_point_cloud.points = o3d.utility.Vector3dVector(red_points)
red_point_cloud.paint_uniform_color([1, 0, 0])  # Red color

green_point_cloud = o3d.geometry.PointCloud()
green_point_cloud.points = o3d.utility.Vector3dVector(green_points)
green_point_cloud.paint_uniform_color([0, 1, 0])  # Green color

# Merge the two point clouds
merged_point_cloud = red_point_cloud + green_point_cloud

# Visualize the point cloud
o3d.visualization.draw_geometries([merged_point_cloud])

# Plot the original points
plt.scatter(points_2d[:, 0], points_2d[:, 1], color='blue', marker='o', label='Original Points')

# Plot the Delaunay triangulation
plt.triplot(points_2d[:, 0], points_2d[:, 1], tri.simplices, color='red', label='Delaunay Triangulation')

plt.xlabel('X-axis')
plt.ylabel('Y-axis')
plt.title('Delaunay Triangulation on 2D Points')
plt.legend()
plt.show()