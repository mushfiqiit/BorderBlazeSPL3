from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import StreamingResponse
import matplotlib.pyplot as plt
from io import BytesIO
import numpy as np
import open3d as o3d
from fastapi.middleware.cors import CORSMiddleware
import math
from generate_empty_plot import generate_empty_plot

app = FastAPI()

destination_path = f"uploads/file1.pts"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def KNearestNeighbor(file_path):
    point_cloud= np.loadtxt(file_path, skiprows=1, max_rows=10000)
    # Set z-axis values to zero
    point_cloud[:, 2] = 0
    n=len(point_cloud)
    k=min(100, n-1)
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
        """print("Coordinates of desired point ", end=" ")
        for j in range(0, 3):
                if(j==2):
                    print(point_cloud[nodeToFindNeighbor][j])
                else:
                    print(point_cloud[nodeToFindNeighbor][j], end=" ")"""
        totalDistance=0.0
        for i in range(0, k):
            totalDistance+=neighbors[i][0]
            """print("Distance: ", end=" ")
            print(neighbors[i][0], end="  ")
            print("Index: ", end=" ")
            print(neighbors[i][1], end="  ")
            print("Coordinates: ", end=" ")
            for j in range(0, 3):
                if(j==2):
                    print(point_cloud[neighbors[i][1]][j])
                else:
                    print(point_cloud[neighbors[i][1]][j], end=" ")"""
        averageDistance.append(totalDistance/k)

    sumOfAverageKDistances=0.0
    for item in averageDistance:
        sumOfAverageKDistances+=item
    threshold=1.15*(sumOfAverageKDistances/n)
    isBoundaryPoint=[]
    for i in range(0, n):
        if(averageDistance[i]>threshold):
            isBoundaryPoint.append(1)
        else:
            isBoundaryPoint.append(0)
    return isBoundaryPoint


@app.get("/method/1/")
async def neighborhoodapproach():
    isBoundaryPoint=KNearestNeighbor(destination_path)
    point_cloud_data = np.loadtxt(destination_path, skiprows=1, max_rows=10000)
    point_cloud_data[:, 2] = 0
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

    # Extract X, Y, Z coordinates from the point cloud data
    x = point_cloud_data[:, 0]
    y = point_cloud_data[:, 1]
    z = point_cloud_data[:, 2]
    # Create an array to hold the colors for each point
    colors = []

    # Example condition: If intensity value is greater than 0.5, color the point green, otherwise red

    for item in isBoundaryPoint:
        if item==1:
            colors.append('red')
        else:
            colors.append('green')
    
    empty_plot_buffer = generate_empty_plot(x, y, z, colors)

    # Return the empty plot as part of the API response
    return StreamingResponse(empty_plot_buffer, media_type="image/png")

