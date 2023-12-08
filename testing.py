import open3d as o3d
import numpy as np
import math

destination_path = f"build4.pts"

def KNearestNeighbor(file_path):
    point_cloud= np.loadtxt(file_path, skiprows=1, max_rows=10000)
    # Set z-axis values to zero
    point_cloud[:, 2] = 0
    n=len(point_cloud)
    k=min(250, n-1)
    averageDistance=[]
    for nodeToFindNeighbor in range(0, n):
        ##print(nodeToFindNeighbor)
        neighbors=[]

        for i in range(0, n):
            distanceOfNodeI=0.0
            if(i==nodeToFindNeighbor):
                    continue
            for j in range(0, 3):
                distanceOfNodeI+=(point_cloud[i][j]-point_cloud[nodeToFindNeighbor][j])*(point_cloud[i][j]-point_cloud[nodeToFindNeighbor][j])
            distanceOfNodeI=math.sqrt(distanceOfNodeI)
            neighbors.append([distanceOfNodeI, i])
        neighbors.sort()
        totalDistance=0.0
        for i in range(0, k):
            totalDistance+=neighbors[i][0]
        averageDistance.append(totalDistance/k)
    sumOfAverageKDistances=0.0
    for item in averageDistance:
        sumOfAverageKDistances+=item
    threshold=sumOfAverageKDistances/n
    isBoundaryPoint=[]
    for i in range(0, n):
        if(averageDistance[i]>threshold):
            isBoundaryPoint.append(1)
        else:
            isBoundaryPoint.append(0)
    return isBoundaryPoint

isBoundaryPoint=KNearestNeighbor(destination_path)

point_cloud_data = np.loadtxt(destination_path, skiprows=1, max_rows=10000)
n=len(point_cloud_data)
point_cloud_data = point_cloud_data[:, :3]
red_points=[]
green_points=[]
for i in range(n):
    if(isBoundaryPoint[i]==1):
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