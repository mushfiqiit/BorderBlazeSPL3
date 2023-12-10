import numpy as np
from delaunay2D import Delaunay2D
from collections import defaultdict
import open3d as o3d

destination_path="build4.pts"

point_cloud_data = np.loadtxt(destination_path, skiprows=1, max_rows=10000)
n = len(point_cloud_data)
point_cloud_data[:, 2] = 0
point_cloud_data = point_cloud_data[:, :3]
points_2d = []

for i in range(n):
    points_2d.append([point_cloud_data[i][0], point_cloud_data[i][1]])

points_2d = np.array(points_2d)  # Convert to NumPy array

# Create a random set of 2D points
seeds = np.random.random((n, 2))

# Create Delaunay Triangulation and insert points one by one
dt = Delaunay2D()

for i in range (0,n):
    seeds[i][0]=points_2d[i][0]/1000
    seeds[i][1]=points_2d[i][1]/1000

for s in seeds:
    dt.addPoint(s)

#print ("Delaunay triangles:\n", dt.exportTriangles())
triangles=dt.exportTriangles()

# Create a dictionary to store the count for each edge
edge_triangle_count = defaultdict(int)

for triangle in triangles:
    for i in range(3):  # A triangle has three edges
        edge = tuple(sorted([triangle[i], triangle[(i + 1) % 3]]))
        print(edge)
        edge_triangle_count[edge] += 1

# Convert the set of edges to a list for easier handling
edges_list = list(edge_triangle_count.keys())

isBoundary = [0] * n

# Identify boundary points
for edge in edges_list:
    point1, point2 = edge
    print(edge_triangle_count[edge])
    if edge_triangle_count[edge]<=2:
        print(edge)
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

