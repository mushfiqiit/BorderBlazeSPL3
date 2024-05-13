# import
from concave_hull import concave_hull, concave_hull_indexes
import numpy as np
from collections import defaultdict
import open3d as o3d

destination_path="build10.pts"

point_cloud_data = np.loadtxt(destination_path, skiprows=1, max_rows=10000)
n = len(point_cloud_data)
point_cloud_data[:, 2] = 0
point_cloud_data = point_cloud_data[:, :3]
points = []

pointindex= defaultdict(int)

for i in range(n):
    points.append([point_cloud_data[i][0], point_cloud_data[i][1]])
    pointindex[(point_cloud_data[i][0], point_cloud_data[i][1])]=i

points = np.array(points)  # Convert to NumPy array

# Compute the concave hull
hull_points = concave_hull(points)  # Adjust the parameter 'alpha' as needed

# Determine the boundary points of the concave hull
boundary_points = concave_hull_indexes(points)

isBoundary = [0] * n
red_points = []
green_points = []

# Retrieve the indices of the boundary points
boundary_indices = np.where(np.isin(np.arange(len(points)), boundary_points))[0]

for boundaryindex in boundary_indices:
    isBoundary[boundaryindex]=1


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

